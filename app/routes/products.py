from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.product import ProductBase, ProductCreate, ProductResponse
from app.crud import products as crud_product

product_router = APIRouter()

# Retrieve all products
@product_router.get(
    "/",
    tags=["STOCK"],
    response_model=List[ProductBase],
    summary="Get all stocked items (Admin or Manager only)",
    status_code=200,
)
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(getDb)):
    return crud_product.get_all_products(db, skip, limit)

# Retrieve a product by ID
@product_router.get(
    "/{id}",
    tags=["STOCK"],
    response_model=ProductResponse,
    summary="Get a stocked item by ID (Admin or Manager only)",
    status_code=200,
)
def get_product(id: int, db: Session = Depends(getDb)):
    return crud_product.get_product_by_id(db, id)

# Create a new product
@product_router.post(
    "/",
    tags=["STOCK"],
    response_model=ProductResponse,
    summary="Add a new stocked item (Admin or Supplier only)",
    status_code=201,
)
def create_product(payload: ProductCreate, db: Session = Depends(getDb)):
    if crud_product.is_product_name_exists(db, payload.product_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with name '{payload.product_name}' already exists.",
        )
    if payload.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product quantity must be greater than 0.",
        )
    return crud_product.create_product(db, payload)
