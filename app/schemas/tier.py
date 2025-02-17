from typing import List, Optional
from pydantic import BaseModel, Field

# Schema for creating a new feeature
class FeatureBase(BaseModel):
    name: str = Field(..., example="Priority Support")
    description: str = Field(..., example="24/7 customer support.")

class FeatureCreate(FeatureBase):
    pass

class Feature(FeatureBase):
    id: int

    class Config:
        from_attributes = True

class TierBase(BaseModel):
    name: str = Field(..., example="Premium")  
    description: str = Field(..., example="Access to all premium features.")  
    amount: float = Field(..., example=49.99)  

# Schema for creating a new tier
class TierCreate(TierBase):    
    features: List[FeatureCreate] 

# Schema for updating a tier
class TierUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Enterprise") 
    description: Optional[str] = Field(None, example="Updated description for Enterprise tier.")  
    amount: Optional[float] = Field(None, example=99.99) 
    features: Optional[List[FeatureCreate]] = None  
    
# Schema for tier responses
class TierRes(TierBase):
    id: int
    features: List[Feature] = []
    
    class Config:
        from_attributes = True

""" 
TierUpdate:
Adjust the amount of a subscription tier when prices change.
Update the description to reflect new benefits.
"""