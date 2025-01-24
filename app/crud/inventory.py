from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.inventory import Inventory

# Helper function to fetch an inventory by ID
def get_inventory_by_id(db: Session, inventory_id: int) -> Inventory:
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory record with ID {inventory_id} not found."
        )
    return inventory

# Retrieve all inventory records
def get_all_inventories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Inventory).offset(skip).limit(limit).all()
