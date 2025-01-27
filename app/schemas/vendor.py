from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class VendorBase(BaseModel):
    company_id: int = Field(..., example=1, description="ID of the associated company")
    name: Optional[str] = Field(None, example="John Doe", description="Name of the vendor")
    email: EmailStr = Field(..., example="vendor@example.com", description="Email address of the vendor")
    address: str = Field(..., example="123 Main Street, City, Country", description="Vendor's address")
    tel_no: str = Field(..., example="+1234567890", description="Vendor's phone number (unique)")
    avatar: Optional[str] = Field(None, example="https://example.com/avatar.png", description="URL of the vendor's avatar image")
    status: Optional[str] = Field(default="Completed", example="Active", description="Vendor's status")

class VendorCreate(VendorBase):
    password_hash: str = Field(..., example="strongpassword123", description="Password for the vendor account")

class VendorUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated name of the vendor")
    address: Optional[str] = Field(None, description="Updated address of the vendor")
    tel_no: Optional[str] = Field(None, description="Updated phone number of the vendor")
    avatar: Optional[str] = Field(None, description="Updated avatar URL for the vendor")
    status: Optional[str] = Field(None, description="Updated status of the vendor")

class VendorResponse(VendorBase):
    id: int = Field(..., example=1, description="Unique identifier for the vendor record")
    createdAt: datetime = Field(..., example="2024-01-01T12:00:00", description="Timestamp when the vendor was created")

    class Config:
        from_attributes = True
