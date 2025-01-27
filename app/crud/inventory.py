from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.inventory import Inventory
from app.models.products import Product
from app.schemas.inventory import InventoryAdjust, InventoryCreate, InventoryUpdate

# Helper function to fetch an inventory by ID
def get_inventory_by_id(db: Session, inventory_id: int) -> Inventory:
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory record with ID {inventory_id} not found."
        )
    return inventory

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
def get_all_inventories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Inventory).offset(skip).limit(limit).all()

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
        setattr(inventory_item, key, value)  # Dynamically update fields

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

# Create or update inventory record (handle stock adjustments)
def manage_inventory(db: Session, payload: InventoryCreate):
    # Fetch product by ID and serial number
    product = db.query(Product).filter(
        Product.id == payload.product_id,
        Product.serial_no == payload.serial_no,
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
        Inventory.product_id == payload.product_id,
        Inventory.serial_no == payload.serial_no,
    ).first()

    try:
        if inventory_item:
            # Update existing inventory record
            inventory_item.quantity += payload.quantity
        else:
            # Create a new inventory record
            inventory_item = Inventory(
                company_id=product.company_id,
                product_id=product.id,
                quantity=payload.quantity,
                base_price=product.b_p,
                selling_price=float(product.b_p) * 1.2,  # Markup
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

# Restock product from inventory
def restock_product(db: Session, inventory_id: int, quantity: int):
    # Validate quantity
    if quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be at least 1.",
        )
    
    # Fetch inventory item and product
    inventory_item = get_inventory_by_id(db, inventory_id)
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
    inventory_item = get_inventory_by_id(db, inventory_id)
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
    inventory_item = get_inventory_by_id(db, inventory_id)
    product = get_product_by_id(db, inventory_item.product_id)

    if inventory_item.quantity - payload.adjustment < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adjustment would result in negative inventory stock."
        )

    inventory_item.quantity -= payload.adjustment
    product.quantity += payload.adjustment

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