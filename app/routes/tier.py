from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import getDb
from app.crud import tier as crud_tier
from app.schemas.tier import Tier, TierCreate

tier_router = APIRouter()

@tier_router.post(
    "/", 
    response_model=Tier, 
    summary="Create a new tier (Admin only)", 
    status_code=201
)
def create_tier(tier: TierCreate, db: Session = Depends(getDb)):
    return crud_tier.create_tier(db, tier)

@tier_router.get(
    "/", 
    response_model=list[Tier], 
    summary="Retrieve a list of tiers", 
    status_code=200
)
def get_tiers(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    return crud_tier.get_tiers(db, skip=skip, limit=limit)

@tier_router.get(
    "/{tier_id}", 
    response_model=Tier, 
    summary="Retrieve a specific tier by ID", 
    status_code=200
)
def get_tier(tier_id: int, db: Session = Depends(getDb)):
    tier = crud_tier.get_tier(db, tier_id)
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    return tier
