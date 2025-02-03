from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, File, HTTPException, UploadFile, status
from app.dependencies.auth import get_current_user_with_role
from app.models.company import Company
from app.models.inventory import Inventory
from app.models.products import Product
from app.models.vendors import Vendor
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.user import User
from app.utils.file_utils import save_upload_file

# Helper function to fetch a product by ID
def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product

# Helper function to check if a record exists
def record_exists(db: Session, model, **filters) -> bool:
    return db.query(model).filter_by(**filters).first() is not None

# Retrieve all products with pagination
def get_all_products(
    db: Session, skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user_with_role("admin"))
):
    return (
        db.query(Product)
        .filter(Product.company_id == current_user.company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

# Create a new product
def create_product(db: Session, product: ProductCreate, image: Optional[UploadFile] = File(None)):
    # Ensure the company exists
    if not record_exists(db, Company, id=product.company_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Company with ID {product.company_id} does not exist."
        )
    
    # Ensure the vendor exists
    if not record_exists(db, Vendor, id=product.vendor_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vendor with ID {product.vendor_id} does not exist."
        )

    # Ensure the product name is unique
    if record_exists(db, Product, product_name=product.product_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with name '{product.product_name}' already exists."
        )
    
    # Handle image upload if provided
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must be an image."
            )
        product.image =  save_upload_file(image)

    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Update a product
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

# Delete a product with inventory check
def delete_product(db: Session, product_id: int, force: bool = False) -> dict:
    product = get_product_by_id(db, product_id)

    # Fetch inventory items linked to the product
    inventory_items = db.query(Inventory).filter(Inventory.product_id == product_id).all()

    if inventory_items and not force:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a product with inventory. Use 'force=true' to delete."
        )

    if product.quantity > 0 and not force:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a product with remaining stock. Use 'force=true' to delete."
        )

    try:
        # If force is True, delete inventory items
        for item in inventory_items:
            db.delete(item)

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
