from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import getDb
from app.models.vendors import Vendor
from app.schemas.vendor import VendorResponse

vendor_router = APIRouter()

# Retrieve all vendors
@vendor_router.get(
    "/",
    tags=["VENDORS"],
    response_model=List[VendorResponse],
    summary="Retrieve all vendor records (Admin Or Manager only)",
    status_code=200,
)
def get_vendors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(getDb)
):
    vendors = db.query(Vendor).offset(skip).limit(limit).all()
    return vendors
