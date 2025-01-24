from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import getDb
from app.models.sales import Sale
from app.schemas.sales import SalesResponse

sales_router = APIRouter()

# Retrieve all sales
@sales_router.get(
    "/",
    tags=["SALES"],
    response_model=List[SalesResponse],
    summary="Retrieve all sales records (Admin Or Manager only)",
    status_code=200,
)
def get_sales(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(getDb)):
    sales = db.query(Sale).offset(skip).limit(limit).all()
    return sales