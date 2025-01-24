from typing import Optional
from pydantic import BaseModel, Field

class TierBase(BaseModel):
    name: str = Field(..., example="Premium")  #"Premium"
    description: str = Field(..., example="Access to all premium features.")  #Brief tier description
    amount: float = Field(..., example=49.99)  #Price of the tier

# Schema for creating a new tier
class TierCreate(TierBase):
    pass

# Schema for updating a tier
class TierUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Enterprise")  # Allow updating the name
    description: Optional[str] = Field(None, example="Updated description for Enterprise tier.")  # Allow updating description
    amount: Optional[float] = Field(None, example=99.99)  # Allow updating price
# Schema for tier responses
class Tier(TierBase):
    id: int = Field(..., example=1)  #Unique tier ID

    class Config:
        from_attributes = True

""" 
TierUpdate:
Adjust the amount of a subscription tier when prices change.
Update the description to reflect new benefits.
"""