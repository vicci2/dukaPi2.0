from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import getDb
from app.models.products import Product
from app.schemas.product import ProductBase

product_router = APIRouter()

# Retrieve all products
@product_router.get(
    "/",
    tags=["STOCK"],
    response_model=List[ProductBase],
    summary="Get all stocked items (Admin or Manager only)",
    status_code=200
)
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(getDb)):
    """
    Retrieve all stocked products.
    """
    return db.query(Product).all()