from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import getDb
from app.dependencies.auth import get_current_user, get_current_user_with_role
from app.models.inventory import Inventory
from app.models.user import User
from app.schemas.inventory import InventoryAdjust, InventoryCreate, InventoryResponse, InventoryUpdate, Item
from app.crud import inventory as crud_inventory
from app.schemas.product import ProductAvail

inventory_router = APIRouter()

@inventory_router.get(
    "/",
    response_model=List[InventoryResponse],
    summary="Retrieve all inventory records (Anyone but supplier)",
    status_code=200,
)
def get_inventories(skip: int = 0, limit: int = 10, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager", "staff"))):
    """
    Retrieve a list of inventory records with pagination.
    """
    return crud_inventory.get_all_inventories(db, current_user)

# Retrieve a single inventory record
@inventory_router.get(
    "/{id}",
    response_model=InventoryResponse,
    summary="Retrieve a single inventory record",
    status_code=200,
)
def get_inventory(id: int, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager", "staff"))):
    """
    Retrieve details of a single inventory record by its ID.
    """
    return crud_inventory.get_inventory_by_id(db, id, current_user)

# Update an existing inventory record
@inventory_router.put(
    "/{id}",
    response_model=InventoryResponse,
    summary="Update an existing inventory record (Admin Or Manager only)",
    status_code=200
)
def update_inventory(id: int, payload: InventoryUpdate, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Update an existing inventory record by its ID.
    """
    return crud_inventory.update_inventory(db, id, payload,current_user)

# Delete an inventory record
@inventory_router.delete(
    "/{id}",
    response_model=dict,
    summary="Delete an inventory record (Admin only)",
    status_code=200
)
def delete_inventory(id: int, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin"))):
    """
    Delete an inventory record by its ID.
    """
    return crud_inventory.delete_inventory(db, id)

# Restock product from inventory
@inventory_router.post(
    "/{id}/restock",
    response_model=dict,
    summary="Restock product from inventory (Admin or Manager only)",
    status_code=200,
)
def restock_product(id: int, quantity: int, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Restock product by transferring stock from inventory to the product's stock.
    """
    return crud_inventory.restock_product(db, id, quantity)

# Adjust inventory (increase stock levels)
@inventory_router.patch(
    "/{id}/increase",
    response_model= ProductAvail,
    summary="Increase inventory stock levels (Admin or Manager only)",
    status_code=200,
)
def increase_inventory(id: int, payload: InventoryAdjust, db: Session = Depends(getDb),  current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Increase inventory stock levels with positive adjustment.
    """
    return crud_inventory.increase_inventory(db, id, payload, current_user)

# Force reduce inventory (decrease stock levels)
@inventory_router.patch(
    "/{id}/reduce",
    response_model= ProductAvail,
    summary="Force reduce inventory stock levels (Admin or Manager only)",
    status_code=200,
)
def reduce_inventory(id: int, payload: InventoryAdjust, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Force reduce inventory stock levels (including negative stock).
    """
    return crud_inventory.reduce_inventory(db, id, payload, current_user)