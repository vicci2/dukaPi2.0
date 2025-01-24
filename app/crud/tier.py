from sqlalchemy.orm import Session
from app.models.tier import Tier
from app.schemas.tier import TierCreate

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
