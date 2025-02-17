from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Base schema for company-related properties
class CompanyBase(BaseModel):
    name: str = Field(..., example="Founders") 
    phone: str = Field(..., example="+1234567890") 
    email: EmailStr = Field(..., example="contact@founders.com") 

# Schema for creating a new company
class CompanyCreate(CompanyBase):
    pass

# Schema for updating an existing company
class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Founders") 
    phone: Optional[str] = Field(None, example="+1987654321")
    email: Optional[EmailStr] = Field(None, example="updated_contact@founders.com")
    location: Optional[str] = Field(None, example="456 Elm St, Metropolis")

# Schema for company responses
class CompanyRes(CompanyBase):
    id: int = Field(..., example=1) 
    location: Optional[str] = Field(None, example="123 Main St, Springfield")  

    class Config:
        from_attributes = True
