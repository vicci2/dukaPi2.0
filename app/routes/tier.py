from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import getDb
from app.crud import tier as crud_tier
from app.dependencies.auth import get_current_user_with_role
from app.models.user import User
from app.schemas.tier import TierRes, TierCreate, TierUpdate

tier_router = APIRouter()

@tier_router.post(
    "/", 
    response_model=TierRes, 
    summary="Create a new tier (Admin only)", 
    status_code=201
)
def create_tier(tier: TierCreate, db: Session = Depends(getDb)):
    return crud_tier.create_tier(db, tier)

@tier_router.get(
    "/", 
    response_model=list[TierRes], 
    summary="Retrieve a list of tiers", 
    status_code=200
)
def get_tiers(db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin"))):
    return crud_tier.get_tiers(db)

@tier_router.get(
    "/{tier_id}", 
    response_model=TierRes, 
    summary="Retrieve a specific tier by ID", 
    status_code=200
)
def get_tier(tier_id: int, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin"))):
    tier = crud_tier.get_tier(db, tier_id)
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    return tier

@tier_router.put(
    "/{tier_id}", 
    response_model=TierRes, 
    summary="Update a tier (Admin only)", 
    status_code=200
)
def update_tier(
    tier_id: int, 
    tier_update: TierUpdate, 
    db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin"))
):
    """
    Update details of an existing tier. 
    Can modify the tier name, description, and price.
    """
    updated_tier = crud_tier.update_tier(db, tier_id, tier_update)
    return updated_tier

@tier_router.delete(
    "/{tier_id}", 
    response_model=dict, 
    summary="Delete a tier (Admin only)", 
    status_code=200
)
def delete_tier(
    tier_id: int, 
    db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin"))
):
    """
    Delete a specific tier by ID. Be cautious when deleting tiers as it may affect existing subscriptions.
    """
    result = crud_tier.delete_tier(db, tier_id)
    return result
