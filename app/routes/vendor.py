from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import getDb
from app.dependencies.auth import get_current_user_with_role
from app.models.company import Company
from app.schemas.user import User
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.crud import vendor as crud_vendor

vendor_router = APIRouter()

# Retrieve all vendors
@vendor_router.get(
    "/",
    response_model=List[VendorResponse],
    summary="Retrieve all vendors (Admin or Manager only)",
    status_code=200,
)
def get_vendors(skip: int = 0, limit: int = 10, db: Session = Depends(getDb) ,current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Retrieve a list of all vendors with pagination.
    """
    return crud_vendor.get_all_vendors(db, current_user)

# Retrieve a single vendor by ID
@vendor_router.get(
    "/{id}",
    response_model=VendorResponse,
    summary="Retrieve a single vendor (Admin or Manager only)",
    status_code=200,
)
def get_vendor(id: int, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Retrieve details of a single vendor by its ID.
    """
    return crud_vendor.get_vendor_by_id(db, id)

# Create a new vendor
@vendor_router.post(
    "/",
    response_model=VendorResponse,
    summary="Create a new vendor (Admin only)",
    status_code=201,
)
def create_vendor(vendor_create: VendorCreate, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin"))):
    """
    Create a new vendor in the system.
    """
    if current_user.company_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin does not belong to any company."
        )
    # Check if company exists
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Company with ID {current_user.company_id} does not exist."
        )
    
    return crud_vendor.create_vendor(db, vendor_create)

# Update an existing vendor
@vendor_router.put(
    "/{id}",
    response_model=VendorResponse,
    summary="Update an existing vendor (Admin nd Manager only)",
    status_code=200,
)
def update_vendor(id: int, vendor_update: VendorUpdate, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Update details of an existing vendor by ID.
    """
    return crud_vendor.update_vendor(db, id, vendor_update, )

# Delete a vendor
@vendor_router.delete(
    "/{id}",
    response_model=VendorResponse,
    summary="Delete a vendor (Admin only)",
    status_code=200,
)
def delete_vendor(id: int, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    """
    Delete a vendor by ID.
    """
    return crud_vendor.delete_vendor(db, id, current_user)
