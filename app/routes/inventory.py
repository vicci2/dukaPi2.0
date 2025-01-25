from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.inventory import InventoryAdjust, InventoryCreate, InventoryResponse
from app.crud import inventory as crud_inventory

inventory_router = APIRouter()

@inventory_router.get(
    "/",
    response_model=List[InventoryResponse],
    summary="Retrieve all inventory records (Anyone but supplier)",
    status_code=200,
)
def get_inventories(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    """
    Retrieve a list of inventory records with pagination.
    """
    return crud_inventory.get_all_inventories(db, skip, limit)

@inventory_router.get(
    "/{id}",
    response_model=InventoryResponse,
    summary="Retrieve a single inventory record",
    status_code=200,
)
def get_inventory(id: int, db: Session = Depends(getDb)):
    """
    Retrieve details of a single inventory record by its ID.
    """
    return crud_inventory.get_inventory_by_id(db, id)

# Manage inventory (Create or Update)
@inventory_router.post(
    "/",
    response_model=InventoryResponse,
    summary="Create or Update inventory record (Admin only)",
    status_code=201,
)
def manage_inventory(payload: InventoryCreate, db: Session = Depends(getDb)):
    """
    Create or update inventory record and handle stock adjustments.
    """
    return crud_inventory.manage_inventory(db, payload)

# Restock product from inventory
@inventory_router.post(
    "/{id}/restock",
    response_model=dict,
    summary="Restock product from inventory (Admin or Manager only)",
    status_code=200,
)
def restock_product(id: int, quantity: int, db: Session = Depends(getDb)):
    """
    Restock product by transferring stock from inventory to the product's stock.
    """
    return crud_inventory.restock_product(db, id, quantity)

# Adjust inventory (increase stock levels)
@inventory_router.patch(
    "/{id}/increase",
    response_model=InventoryResponse,
    summary="Increase inventory stock levels (Admin or Manager only)",
    status_code=200,
)
def increase_inventory(id: int, payload: InventoryAdjust, db: Session = Depends(getDb)):
    """
    Increase inventory stock levels with positive adjustment.
    """
    return crud_inventory.increase_inventory(db, id, payload)

# Force reduce inventory (decrease stock levels)
@inventory_router.patch(
    "/{id}/reduce",
    response_model=InventoryResponse,
    summary="Force reduce inventory stock levels (Admin or Manager only)",
    status_code=200,
)
def reduce_inventory(id: int, payload: InventoryAdjust, db: Session = Depends(getDb)):
    """
    Force reduce inventory stock levels (including negative stock).
    """
    return crud_inventory.reduce_inventory(db, id, payload)