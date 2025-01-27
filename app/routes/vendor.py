from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import getDb
from app.models.company import Company
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
def get_vendors(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    """
    Retrieve a list of all vendors with pagination.
    """
    return crud_vendor.get_all_vendors(db, skip, limit)

# Retrieve a single vendor by ID
@vendor_router.get(
    "/{id}",
    response_model=VendorResponse,
    summary="Retrieve a single vendor (Admin or Manager only)",
    status_code=200,
)
def get_vendor(id: int, db: Session = Depends(getDb)):
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
def create_vendor(vendor_create: VendorCreate, db: Session = Depends(getDb)):
    """
    Create a new vendor in the system.
    """
    # Check if company exists
    company = db.query(Company).filter(Company.id == vendor_create.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Company with ID {vendor_create.company_id} does not exist."
        )
    
    return crud_vendor.create_vendor(db, vendor_create)

# Update an existing vendor
@vendor_router.put(
    "/{id}",
    response_model=VendorResponse,
    summary="Update an existing vendor (Admin only)",
    status_code=200,
)
def update_vendor(id: int, vendor_update: VendorUpdate, db: Session = Depends(getDb)):
    """
    Update details of an existing vendor by ID.
    """
    return crud_vendor.update_vendor(db, id, vendor_update)

# Delete a vendor
@vendor_router.delete(
    "/{id}",
    response_model=VendorResponse,
    summary="Delete a vendor (Admin only)",
    status_code=200,
)
def delete_vendor(id: int, db: Session = Depends(getDb)):
    """
    Delete a vendor by ID.
    """
    return crud_vendor.delete_vendor(db, id)
