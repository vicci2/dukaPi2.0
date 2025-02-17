from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, File, HTTPException, UploadFile, status
from app.dependencies.auth import get_current_user_with_role
from app.models.company import Company
from app.models.inventory import Inventory
from app.models.products import Product
from app.models.vendors import Vendor
from app.schemas.inventory import InventoryCreate
from app.schemas.product import ProductAvail, ProductCreate, ProductUpdate
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
# def create_product(db: Session, product: ProductCreate, image: Optional[UploadFile] = File(None)):
def create_product(db: Session, product: ProductCreate):
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
    
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

    # Handle image upload if provided
    # if image:
    #     if not image.content_type.startswith("image/"):
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="Uploaded file must be an image."
    #         )
    #     product.image =  save_upload_file(image)

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

# Avail or update inventory record (handle stock adjustments)
def avail(id: int, db: Session, payload: ProductAvail):
    # Fetch product by ID and serial number
    product = db.query(Product).filter(
        Product.id == id,
        # serial_no=payload.serial_no,
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with specified ID and serial number does not exist.",
        )

    if product.quantity < payload.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient quantity for product '{product.product_name}'.",
        )

    # Check if an inventory record already exists for the product and serial number
    inventory_item = db.query(Inventory).filter(
        Inventory.product_id == id,
        Inventory.serial_no == payload.serial_no,
    ).first()

    try:
        if inventory_item:
            # Update existing inventory record
            inventory_item.quantity += payload.quantity
        else:
            # Create a new inventory record (Avail)
            inventory_item = Inventory(
                company_id=product.company_id,
                product_id=product.id,
                quantity=payload.quantity,
                base_price=product.b_p,
                selling_price=float(product.b_p) * 1.2,
                serial_no=product.serial_no,
            )
            db.add(inventory_item)

        # Deduct from product stock
        product.quantity -= payload.quantity

        # Commit changes
        db.commit()
        db.refresh(inventory_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to manage inventory: {str(e)}",
        )

    return inventory_item

# Delete a product with inventory check
def delete_product(db: Session, product_id: int,) -> dict:
    product = get_product_by_id(db, product_id)

    # Fetch inventory items linked to the product
    inventory_items = db.query(Inventory).filter(Inventory.product_id == product_id).all()

    if inventory_items :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a product with inventory. Use 'force=true' to delete."
        )

    # if product.quantity > 0 :
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Cannot delete a product with remaining stock. Use 'force=true' to delete."
    #     )

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
