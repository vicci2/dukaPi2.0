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

# Helper function to check if a record exists (optional, for reuse)
def record_exists(db: Session, model, **filters) -> bool:
    return db.query(model).filter_by(**filters).first() is not None

# Retrieve all vendors
def get_all_vendors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Vendor).offset(skip).limit(limit).all()

# Create a new vendor
def create_vendor(db: Session, vendor_create: VendorCreate):
    # Optionally, check for uniqueness or required conditions here
    new_vendor = Vendor(**vendor_create.dict())
    db.add(new_vendor)
    try:
        db.commit()
        db.refresh(new_vendor)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create vendor: {str(e)}"
        )
    return new_vendor

# Update an existing vendor
def update_vendor(db: Session, vendor_id: int, vendor_update: VendorUpdate):
    db_vendor = get_vendor_by_id(db, vendor_id)
    for key, value in vendor_update.dict(exclude_unset=True).items():
        setattr(db_vendor, key, value)
    try:
        db.commit()
        db.refresh(db_vendor)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update vendor: {str(e)}"
        )
    return db_vendor

# Delete a vendor
def delete_vendor(db: Session, vendor_id: int):
    db_vendor = get_vendor_by_id(db, vendor_id)
    try:
        db.delete(db_vendor)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete vendor: {str(e)}"
        )
    return {"message": f"Vendor with ID {vendor_id} successfully deleted."}
