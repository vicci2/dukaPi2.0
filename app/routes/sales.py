from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.sales import SalesCreate, SalesResponse, SalesUpdate
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

# Create a new sale
@sales_router.post(
    "/",
    response_model=SalesResponse,
    summary="Record a new sale (Admin, Manager & Staff only)",
    status_code=201
)
def create_sale(payload: SalesCreate, db: Session = Depends(getDb)):
    """
    Record a new sale and deduct inventory stock.
    """
    new_sale = crud_sales.create_sale(db, payload)
    return new_sale

# Update a sale
@sales_router.put(
    "/{id}",
    response_model=SalesResponse,
    summary="Update a sale record (Admin Or Manager only)",
    status_code=200,
)
def update_sale(
    id: int,
    payload: SalesUpdate,
    db: Session = Depends(getDb)
    ):
    sale = crud_sales.get_sale_by_id(db, id)
    updated_sale = crud_sales.update_sale(db, sale, payload)
    return updated_sale

# Delete a sale
@sales_router.delete(
    "/{id}",
    response_model=dict,
    summary="Delete a sale record (Admin only)",
    status_code=200,
)
def delete_sale(
    id: int,
    db: Session = Depends(getDb)
):
    sale = crud_sales.get_sale_by_id(db, id)
    crud_sales.delete_sale(db, sale)
    return {"message": f"Sale record with ID {id} deleted successfully."}