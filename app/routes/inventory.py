from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import getDb
from app.models.inventory import Inventory
from app.models.products import Product
from app.schemas.inventory import InventoryResponse
from app.schemas.product import ProductBase


inventory_router=APIRouter()

# Retrieve all inventory records

@inventory_router.get(
    "/",
    tags=["INVENTORY"],
    response_model=List[InventoryResponse],
    summary="Retrieve all inventory records (Anyone but supplier)",
    status_code=200
)
def get_inventories(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
# def get_inventories(skip: int = 0, limit: int = 10, db: Session = Depends(getDb), current_user: User = Depends(get_current_user) ):
    """
    Retrieve a list of inventory records with pagination.
    """
    return db.query(Inventory).offset(skip).limit(limit).all()
