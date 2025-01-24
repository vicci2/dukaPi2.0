from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.vendors import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate

# Helper function to fetch a vendor by ID
def get_vendor_by_id(db: Session, vendor_id: int) -> Vendor:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendor with ID {vendor_id} not found."
        )
    return vendor

# Retrieve all vendors
def get_all_vendors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Vendor).offset(skip).limit(limit).all()

# Create a new vendor
def create_vendor(db: Session, vendor_create: VendorCreate):
    db_vendor = Vendor(**vendor_create.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

# Update an existing vendor
def update_vendor(db: Session, vendor_id: int, vendor_update: VendorUpdate):
    db_vendor = get_vendor_by_id(db, vendor_id)
    for key, value in vendor_update.dict(exclude_unset=True).items():
        setattr(db_vendor, key, value)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

# Delete a vendor
def delete_vendor(db: Session, vendor_id: int):
    db_vendor = get_vendor_by_id(db, vendor_id)
    db.delete(db_vendor)
    db.commit()
    return db_vendor
