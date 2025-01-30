from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.company import Company
from app.models.inventory import Inventory
from app.models.products import Product
from app.schemas.product import ProductCreate, ProductUpdate

# Helper function to fetch a product by ID
def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product
    # db.query(Product).filter().offset(skip).limit(limit).all()

# Retrieve all products
def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).filter().offset(skip).limit(limit).all()
    # return db.query(Product).filter().offset(skip).limit(limit).all()

# Create a new product
def create_product(db: Session, product: ProductCreate):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Check if a product name already exists
def is_product_name_exists(db: Session, product_name: str) -> bool:
    return db.query(Product).filter(Product.product_name == product_name).first() is not None

# Check if a company already exists
def is_company_exists(db: Session, company_id: str) -> bool:
    return db.query(Company).filter(Company.id == company_id).first() is not None

def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = get_product_by_id(db, product_id)
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update product: {str(e)}"
        )
    return product

def delete_product(db: Session, product_id: int, force: bool = False) -> dict:
    product = get_product_by_id(db, product_id)
    inventory_items = db.query(Inventory).filter(Inventory.product_id == product_id).all()

    if inventory_items:
        if not force:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a product with inventory. Use 'force=true' to delete."
            )
        for item in inventory_items:
            db.delete(item)

    if product.quantity > 0 and not force:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a product with remaining stock. Use 'force=true' to delete."
        )

    try:
        db.delete(product)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete product: {str(e)}"
        )

    return {
        "message": f"Product '{product.product_name}' successfully removed.",
        "details": {"product_id": product.id, "product_name": product.product_name},
    }
