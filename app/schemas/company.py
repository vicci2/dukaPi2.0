from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Base schema for company-related properties
class CompanyBase(BaseModel):
    name: str = Field(..., example="Founders")  # Example: "Founders"
    phone: str = Field(..., example="+1234567890")  # Example: "+1234567890"
    email: EmailStr = Field(..., example="contact@founders.com")  # Example: "contact@founders.com"
    location: Optional[str] = Field(None, example="123 Main St, Springfield")  # Example: "123 Main St, Springfield"

# Schema for creating a new company
class CompanyCreate(CompanyBase):
    pass

# Schema for updating an existing company
class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Founders")  # Optional for partial updates
    phone: Optional[str] = Field(None, example="+1987654321")
    email: Optional[EmailStr] = Field(None, example="updated_contact@founders.com")
    location: Optional[str] = Field(None, example="456 Elm St, Metropolis")

# Schema for company responses
class Company(CompanyBase):
    id: int = Field(..., example=1)  # Example: Unique identifier for the company

    class Config:
        from_attributes = True
