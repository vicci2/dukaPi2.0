from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.sales import SalesResponse
from app.crud import sale  as crud_sales
sales_router = APIRouter()

# Retrieve all sales records
@sales_router.get(
    "/",
    response_model=List[SalesResponse],
    summary="Retrieve all sales records (Admin Or Manager only)",
    status_code=200,
)
def get_sales(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    """
    Retrieve a list of sales records with pagination.
    """
    return crud_sales.get_all_sales(db, skip, limit)

# Retrieve a single sale record by ID
@sales_router.get(
    "/{id}",
    response_model=SalesResponse,
    summary="Retrieve a single sale record (Admin Or Manager only)",
    status_code=200,
)
def get_sale(id: int, db: Session = Depends(getDb)):
    """
    Retrieve details of a single sale record by its ID.
    """
    return crud_sales.get_sale_by_id(db, id)
