from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.tier import Tier
from app.schemas.tier import TierCreate, TierUpdate

def create_tier(db: Session, tier: TierCreate):
    db_tier = Tier(**tier.dict())
    db.add(db_tier)
    db.commit()
    db.refresh(db_tier)
    return db_tier

def get_tiers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tier).offset(skip).limit(limit).all()

def get_tier(db: Session, tier_id: int):
    return db.query(Tier).filter(Tier.id == tier_id).first()

def update_tier(db: Session, tier_id: int, tier_update: TierUpdate):
    # Fetch the tier
    db_tier = db.query(Tier).filter(Tier.id == tier_id).first()
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    
    # Update the tier fields
    for key, value in tier_update.dict(exclude_unset=True).items():
        setattr(db_tier, key, value)
    
    # Commit the changes
    db.add(db_tier)
    try:
        db.commit()
        db.refresh(db_tier)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update tier: {str(e)}"
        )
    
    return db_tier

def delete_tier(db: Session, tier_id: int):
    db_tier = db.query(Tier).filter(Tier.id == tier_id).first()
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    try:
        db.delete(db_tier)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete tier: {str(e)}"
        )
    
    return {"message": f"Tier with ID {tier_id} deleted successfully."}
