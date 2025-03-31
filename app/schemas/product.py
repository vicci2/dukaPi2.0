from fastapi import File, UploadFile
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base Schema
class ProductBase(BaseModel):
    company_id: int = Field(..., example=1)
    vendor_id: int = Field(..., example=109)
    serial_no: str = Field(..., example="12345-ABC")
    product_name: str = Field(..., example="Laptop")    
    category: Optional[str] = Field(None, example="Electronics")
    desc: str = Field(..., example="A high-performance laptop for gaming and work.")
    quantity: int = Field(..., ge=0, example=100) 
    b_p: float = Field(..., ge=0.0, example=500.00)  
    image: Optional[str] = Field(None, example="https://example.com/avatar.jpg")

# Schema for creating a product
class ProductCreate(ProductBase):
    pass
    # image: Optional[UploadFile] = File(None)  

# Schema for updating a product
class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(None, example="Gaming Laptop")
    category: Optional[str] = Field(None, example="Gaming")
    desc: Optional[str] = Field(None, example="Updated description.")
    quantity: Optional[int] = Field(None, ge=0, example=50)
    b_p: Optional[float] = Field(None, ge=0.0, example=600.00)

# Schema for product availability (quantity)
class ProductAvail(BaseModel):
    company_id: int = Field(..., example=109, description="ID of the related company")
    quantity: int = Field(..., ge=0, example=50, description="Stock quantity to avail")
    base_price: float = Field(..., ge=0.0, example=100.00, description="Base price of the product")
    serial_no: str = Field(..., example="12345-ABC", description="Unique identifier for the inventory item")

# Schema for deleting a product
class ProductDel(BaseModel):
    id: int
    name: str

# Schema for product response (including timestamps)
class ProductResponse(ProductBase):
    id: int = Field(..., example=1)
    date: datetime = Field(..., example="2024-01-01T12:00:00")
    last_updated: Optional[datetime] = Field(None, example="2024-01-02T15:30:00")
    # inventory deets
    inventory_id: Optional[int] = Field(None, example=1)
    selling_price: Optional[float] = Field(None, ge=0.0, example=600.00)
    inventory_quantity: Optional[int] = Field(None, ge=0, example=50)
    inventory_last_updated: Optional[datetime] = Field(..., example = "2024-01-01T12:00:00")
    inventory_created_at: Optional[datetime] = Field(..., example = "2024-01-01T12:00:00")
    total_sales: Optional[int] = Field(None, ge=0, example=50)
    sold_at: Optional[datetime] = Field(..., example = "2024-01-01T12:00:00")
    sale_last_updated: Optional[datetime] = Field(..., example = "2024-01-01T12:00:00")

    class Config:
        from_attributes = True  # Enables compatibility with SQLAlchemy models
