from typing import List
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user, get_current_user_with_role
from app.models.inventory import Inventory
from app.models.products import Product
from app.models.sales import Sale
from app.models.user import User
from app.schemas.inventory import InventoryAdjust, InventoryCreate, InventoryResponse, InventoryUpdate, Item

from typing import List

def format_inventory_response(inventories) -> List[Item]:
    return [
        Item(
                company_id=inventory.company_id,
                id=inventory.id,
                product_id=inventory.product_id,
                product_name=product.product_name,
                image=product.image,
                desc=product.desc,
                base_price=product.b_p,
                last_updated=str(product.last_updated) if product.last_updated else None,  
                createdAt=str(inventory.date) if inventory.date else None, 
                stkQuantity=product.quantity, 
                inQuantity=inventory.quantity,
                salesQtty=getattr(sale, "quantity", 0), 
                selling_price=getattr(sale, "selling_price", inventory.selling_price),
                serial_no=inventory.serial_no,
            )
            for inventory, product, sale in inventories 
    ]

    """ 
    stkQuantity: int
    inQuantity: int
    salesQtty: int
    """

# Helper function to fetch an inventory by ID
def get_inventory_by_id(db: Session, inventory_id: int):
    inventory = (
        db.query(Inventory, Product, Sale)
        .join(Product, Inventory.product_id == Product.id).outerjoin(Sale, Sale.inventory_id == Inventory.id) 
        .filter(Inventory.id == inventory_id)
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory record with ID {inventory_id} not found."
        )

    return format_inventory_response([inventory])[0]  

# Helper function to fetch a product by ID
def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product

# Retrieve all inventory records
def get_all_inventories(
    db: Session, skip: int = 0, limit: int = 10) -> List[InventoryResponse]:
    # Fetch inventories with related product details
    inventories = (
        db.query(Inventory).options(joinedload(Inventory.product)).order_by(Inventory.product_id).offset(skip).limit(limit).all()
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
def update_inventory(db: Session, inventory_id: int, payload: InventoryUpdate) -> Inventory:
    inventory_item = get_inventory_by_id(db, inventory_id)
    
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
    product.quantity += quantity

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
def increase_inventory(db: Session, inventory_id: int, payload: InventoryAdjust):
    inventory_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    product = get_product_by_id(db, inventory_item.product_id)

    if inventory_item.quantity + payload.adjustment < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adjustment would result in negative inventory levels."
        )

    inventory_item.quantity += payload.adjustment
    product.quantity -= payload.adjustment

    try:
        db.commit()
        db.refresh(inventory_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to adjust inventory: {str(e)}",
        )

    return inventory_item

# Force reduce inventory (adjust negative stock)
def reduce_inventory(db: Session, inventory_id: int, payload: InventoryAdjust):
    inventory_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    product = get_product_by_id(db, inventory_item.product_id)

    # Ensure adjustment is negative for reduction
    if payload.adjustment > 0:
        payload.adjustment = -payload.adjustment  # Force negative value

    inventory_item.quantity += payload.adjustment
    product.quantity -= payload.adjustment

    try:
        db.commit()
        db.refresh(inventory_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to force adjust inventory: {str(e)}",
        )

    return inventory_item
