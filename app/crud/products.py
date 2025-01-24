from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.products import Product
from app.schemas.product import ProductCreate

# Helper function to fetch a product by ID
def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product

# Retrieve all products
def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

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
