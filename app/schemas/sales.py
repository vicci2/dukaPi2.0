from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class SalesBase(BaseModel):
    company_id: int = Field(..., example=1, description="ID of the copmpany selling the item")
    inventory_id: int = Field(..., example=1, description="ID of the inventory item being sold")
    quantity: Decimal = Field(..., ge=1, example=10, description="Quantity of the product being sold")
    selling_price: Decimal = Field(..., ge=0.0, example=50.00, description="Selling price per unit")
    base_price: Optional[Decimal] = Field(None, example=40.00, description="Base price during the sale")
    status: Optional[str] = Field(default="Completed", example="Completed", description="Status of the sale")

class SalesCreate(SalesBase):
    pass  # Inherits all fields from SalesBase

class SalesUpdate(BaseModel):
    quantity: Optional[Decimal] = Field(None, ge=1, description="Updated quantity of the product")
    selling_price: Optional[Decimal] = Field(None, ge=0.0, description="Updated selling price per unit")
    status: Optional[str] = Field(None, description="Updated status of the sale")

class SalesResponse(SalesBase):
    id: int = Field(..., example=1, description="Unique identifier for the sale record")
    last_updated: datetime = Field(..., example="2024-01-01T15:00:00", description="Last updated timestamp for the sale record")

    class Config:
        from_attributes = True
