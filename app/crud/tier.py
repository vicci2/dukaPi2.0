from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.tier import Feature, Tier
from app.schemas.tier import TierCreate, TierUpdate

def create_tier(db: Session, tier: TierCreate):
    # Lookep existing features
    existing_features = {feat.name: feat for feat in db.query(Feature).all()} 
    # Create Feature instances dynamically
    feature_instances = [ ]

    for feat in tier.features:
        if feat.name in existing_features:
            feature_instances.append(existing_features[feat.name])
        else:
            # Create a new feature with description
            new_feature = Feature(name=feat.name, description=feat.description, cost=feat.cost)
            db.add(new_feature)
            db.commit()
            db.refresh(new_feature)
            feature_instances.append(new_feature)

    # Create the Tier instance
    db_tier = Tier(
        name = tier.name,
        description = tier.description,
        amount = tier.amount,
        type = tier.type,
        features = feature_instances  
    )
    # db_tier = Tier(**tier.dict())
    db.add(db_tier)
    db.commit()
    db.refresh(db_tier)
    return db_tier

def get_tiers(db: Session):
    tiers = db.query(Tier).offset(0).limit(10).all()
    if not tiers:
        raise HTTPException(status_code=404, detail="No tiers found")
    return tiers

def get_tier(db: Session, tier_id: int):
    return db.query(Tier).filter(Tier.id == tier_id).first()

def update_tier(db: Session, tier_id: int, tier_update: TierUpdate):
    db_tier = db.query(Tier).filter(Tier.id == tier_id).first()
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    for key, value in tier_update.dict(exclude_unset=True).items():
        if key == "features":
            existing_features = {feat.name: feat for feat in db.query(Feature).all()}

            db_tier.features = []

            for feat in value:
                # Ensure `feat` is treated as a dictionary, not an object
                feature_name = feat["name"]
                feature_description = feat["description"]
                
                if feature_name in existing_features:
                    # Reuse existing feature without changes
                    db_tier.features.append(existing_features[feature_name])
                else:
                    # Create a new feature if not found
                    new_feature = Feature(name=feature_name, description=feature_description)
                    db.add(new_feature)
                    db.commit()
                    db.refresh(new_feature)
                    db_tier.features.append(new_feature)
        else:
            # For other fields (name, description, amount), just update directly
            setattr(db_tier, key, value)

    try:
        db.commit()
        db.refresh(db_tier)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update tier: {str(e)}")

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
