from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user, get_current_user_with_role
from app.models.inventory import Inventory
from app.models.products import Product
from app.models.sales import Sale
from app.models.user import User
from app.schemas.inventory import InventoryAdjust, InventoryCreate, InventoryResponse, InventoryUpdate, Item

from typing import List

# Helper function to fetch an inventory by ID
def get_inventory_by_id(db: Session, inventory_id: int, current_user) -> InventoryResponse:
    result = db.query(
        Inventory.id, Inventory.company_id, Inventory.product_id,
        Product.product_name.label("product_name"), Product.image,
        Inventory.quantity, Inventory.base_price, Inventory.selling_price,
        Inventory.serial_no, Inventory.date, Inventory.last_updated
    ).join(Product, Inventory.product_id == Product.id).filter(
        Inventory.id == inventory_id and Inventory.company_id ==current_user.id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory record with ID {inventory_id} not found."
        )

    return InventoryResponse(**result._asdict())  # Convert Row object to dictionary

# Helper function to fetch a product by ID
def get_product_by_id(db: Session, product_id: int, current_user) -> Product:
    product = db.query(Product).filter(Product.id == product_id and Inventory.company_id ==current_user.company_id).offset(0).limit(1).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product

# Retrieve all inventory records
def get_all_inventories(
    db: Session, current_user) -> List[InventoryResponse]:
    # Fetch inventories with related product details
    inventories = (
        db.query(Inventory).options(joinedload(Inventory.product)).filter(Inventory.company_id == current_user.company_id).order_by(Inventory.product_id).offset(0).limit(100).all()
    )

    # Serialize to InventoryResponse, including related product data
    return [
        InventoryResponse(
            id=inv.id,
            company_id=inv.company_id,
            product_id=inv.product_id,
            product_name=inv.product.product_name,
            image=inv.product.image, 
            quantity=inv.quantity,
            base_price=inv.base_price,
            selling_price=inv.selling_price,
            serial_no=inv.serial_no,
            date=inv.date,
            last_updated=inv.last_updated,
        )
        for inv in inventories
    ]

# Update inventory by ID
def update_inventory(db: Session, inventory_id: int, payload: InventoryUpdate, current_user) -> Inventory:
    inventory_item = get_inventory_by_id(db, inventory_id,current_user)
    
    for key, value in payload.dict(exclude_unset=True).items():
        """ if key == "quantity" and value < 2:  # Ensure minimum quantity threshold
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity cannot be less than 2."
            ) """
        if key in ["base_price", "selling_price"] and value <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{key.replace('_', ' ').capitalize()} must be greater than zero."
            )
        setattr(inventory_item, key, value) 

    inventory_item.last_updated = func.now() 

    try:
        db.commit()
        db.refresh(inventory_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update inventory record: {str(e)}"
        )

    return inventory_item

# Delete inventory by ID
def delete_inventory(db: Session, inventory_id: int):
    inventory_item = get_inventory_by_id(db, inventory_id)
    try:
        db.delete(inventory_item)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete inventory record: {str(e)}"
        )
    return {"message": f"Inventory record with ID {inventory_id} deleted successfully."}

# Restock product from inventory
def restock_product(db: Session, inventory_id: int, quantity: int):
    # Validate quantity
    if quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be at least 1.",
        )
    
    # Fetch inventory item and product
    inventory_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {inventory_id} not found.",
        )
    
    product = get_product_by_id(db, inventory_item.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product associated with inventory ID {inventory_id} not found.",
        )

    # Check inventory availability
    if inventory_item.quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient inventory stock. Available: {inventory_item.quantity}, Requested: {quantity}.",
        )

    # Update stock
    inventory_item.quantity -= quantity
    product.last_updated = func.now()
    inventory_item.last_updated = func.now()

    try:
        db.commit()
        db.refresh(inventory_item)
        db.refresh(product)
    except Exception as e:
        db.rollback()
        # Log the error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to restock product. Please try again later.",
        )

    return {
        "message": f"Restocked {quantity} units of product '{product.product_name}'.",
        "remaining_inventory_stock": inventory_item.quantity,
        "updated_product_stock": product.quantity,
    }

# Increase inventory (adjust positive stock levels)
def increase_inventory(db: Session, inventory_id: int, payload: InventoryAdjust, current_user):
    inventory_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found.")

    product = get_product_by_id(db, inventory_item.product_id, current_user)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if payload.adjustment > product.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available to increase inventory."
        )

    # Adjust inventory levels
    inventory_item.quantity += payload.adjustment
    product.quantity -= payload.adjustment 
    product.last_updated = func.now()
    inventory_item.last_updated = func.now()

    try:
        db.commit()
        db.refresh(inventory_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to adjust inventory: {str(e)}"
        )

    return inventory_item

# Force reduce inventory (adjust negative stock)
def reduce_inventory(db: Session, inventory_id: int, payload: InventoryAdjust, current_user):
    # Fetch inventory item
    inventory_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found.")

    # Fetch product associated with the inventory item
    product = get_product_by_id(db, inventory_item.product_id, current_user)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    # Ensure the adjustment is negative
    adjustment = -abs(payload.adjustment)  
    product.last_updated = func.now()

    # Check if adjustment would make inventory levels go negative
    if inventory_item.quantity + adjustment < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adjustment would result in negative inventory levels."
        )

    inventory_item.quantity += adjustment
    product.quantity += adjustment  
    product.last_updated = func.now()
    inventory_item.last_updated = func.now()
    # Commit changes
    try:
        db.commit()
        db.refresh(inventory_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to adjust inventory: {str(e)}"
        )

    return inventory_item
