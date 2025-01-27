from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InventoryBase(BaseModel):
    company_id: int = Field(..., example=109, description="ID of the related company")
    product_id: int = Field(..., example=1, description="ID of the related product")
    quantity: int = Field(..., ge=0, example=50, description="Stock quantity available")
    base_price: float = Field(..., ge=0.0, example=100.00, description="Base price of the product")
    serial_no: str = Field(..., example="12345-ABC", description="Unique identifier for the inventory item")

class InventoryCreate(InventoryBase):
    pass  # Inherits all fields from InventoryBase

class InventoryUpdate(BaseModel):
    # quantity: Optional[int] = Field(None, ge=0, description="Updated stock quantity")
    base_price: Optional[float] = Field(None, ge=0.0, description="Updated base price")
    selling_price: Optional[float] = Field(None, ge=0.0, description="Updated selling price")

class InventoryAdjust(BaseModel):
    adjustment: int = Field(..., description="Adjustment to stock quantity, positive or negative")

class InventoryResponse(InventoryBase):
    id: int = Field(..., example=1, description="Unique identifier for the inventory record")
    date: datetime = Field(..., example="2024-01-01T12:00:00", description="Timestamp for inventory record creation")
    last_updated: Optional[datetime] = Field(None, example="2024-01-02T15:30:00", description="Timestamp for the last update")

    class Config:
        from_attributes = True  # Ensures compatibility with SQLAlchemy models
