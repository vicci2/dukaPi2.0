from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base Schema
class ProductBase(BaseModel):
    company_id: int = Field(..., example=1)
    vendor_id: int = Field(..., example=109)
    serial_no: str = Field(..., example="12345-ABC")
    # serial_no: str = Field(..., example="12345-ABC", regex=r'^\d{5}-[A-Z]{3}$')
    product_name: str = Field(..., example="Laptop")
    image: Optional[str] = Field(None, example="https://example.com/laptop.jpg")
    category: Optional[str] = Field(None, example="Electronics")
    desc: str = Field(..., example="A high-performance laptop for gaming and work.")
    quantity: int = Field(..., ge=0, example=100) 
    b_p: float = Field(..., ge=0.0, example=500.00)  

# Schema for creating a product
class ProductCreate(ProductBase):
    pass  

# Schema for updating a product
class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(None, example="Gaming Laptop")
    category: Optional[str] = Field(None, example="Gaming")
    desc: Optional[str] = Field(None, example="Updated description.")
    quantity: Optional[int] = Field(None, ge=0, example=50)
    b_p: Optional[float] = Field(None, ge=0.0, example=600.00)

# Schema for product availability (quantity)
class ProductAvail(BaseModel):
    id: int
    quantity: int

# Schema for deleting a product
class ProductDel(BaseModel):
    id: int
    name: str

# Schema for product response (including timestamps)
class ProductResponse(ProductBase):
    id: int = Field(..., example=1)
    date: datetime = Field(..., example="2024-01-01T12:00:00")
    last_updated: Optional[datetime] = Field(None, example="2024-01-02T15:30:00")

    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy models
