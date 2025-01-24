from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.inventory import InventoryResponse
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
