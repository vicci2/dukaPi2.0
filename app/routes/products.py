from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import getDb
from app.dependencies.auth import get_current_user, get_current_user_with_role
from app.schemas.product import ProductBase, ProductCreate, ProductUpdate, ProductResponse
from app.crud import products as crud_product
from app.schemas.user import User

product_router = APIRouter()

# Retrieve all products
@product_router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Get all stocked items (Admin or Manager only)",
    status_code=200,
)
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(getDb),current_user: User = Depends(get_current_user_with_role("admin"))):
    """
    Retrieve all products with pagination.
    """
    return crud_product.get_all_products(db, skip, limit, current_user)

# Retrieve a product by ID
@product_router.get(
    "/{id}",
    response_model=ProductResponse,
    summary="Get a stocked item by ID (Admin or Manager only)",
    status_code=200,
)
def get_product(id: int, db: Session = Depends(getDb)):
    """
    Retrieve a product by its ID.
    """
    return crud_product.get_product_by_id(db, id)

# Create a new product
@product_router.post(
    "/",
    response_model=ProductResponse,
    summary="Add a new stocked item (Admin or Supplier only)",
    status_code=201,
)
def create_product(payload: ProductCreate, image: Optional[UploadFile] = File(None), db: Session = Depends(getDb)):
    """
    Add a new product to the database.
    """
    return crud_product.create_product(db, payload, image)

# Update an existing product
@product_router.put(
    "/{id}",
    response_model=ProductResponse,
    summary="Update an existing product (Admin or Manager only)",
    status_code=200,
)
def update_product(id: int, payload: ProductUpdate, db: Session = Depends(getDb)):
    """
    Update product details by ID.
    """
    return crud_product.update_product(db, id, payload)

# Delete a product
@product_router.delete(
    "/{id}",
    response_model=dict,
    summary="Delete a stocked item (Admin only)",
    status_code=200,
)
def delete_product(id: int, force: bool = False, db: Session = Depends(getDb)):
    """
    Delete a product by its ID, optionally forcing deletion if stock exists.
    """
    return crud_product.delete_product(db, id, force)
