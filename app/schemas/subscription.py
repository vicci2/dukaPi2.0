from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    company_id: int = Field(..., example=1) 
    tier_id: int = Field(..., example=2)  #
    transaction_code: str = Field(..., example="TX12345ABC")  

# Schema for creating a subscription
class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    company_id: Optional[int] = Field(None, example=1)  
    tier_id: Optional[int] = Field(None, example=2) 
    transaction_code: Optional[str] = Field(None, example="TX67890DEF")
    status: Optional[str] = None

# Schema for subscription responses
class SubscriptionRes(SubscriptionBase):
    status: Optional[str] = None
    created_at: Optional[datetime] = Field(None, example="2025-01-01T12:00:00")  # Example: Timestamp of creation

    class Config:
        from_attributes = True

""" 
SubscriptionUpdate:
Update only the tier_id when upgrading a company to a new subscription tier.
Change the transaction_code if a correction is required.
"""