import datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.models.tier import Tier
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate

# Helper function to validate tier ID
def validate_tier(db: Session, tier_id: int):
    tier = db.query(Tier).filter(Tier.id == tier_id).first()
    if not tier:
        raise HTTPException(
            status_code=400, detail=f"Tier ID {tier_id} does not exist."
        )

# Check if a company already has an active subscription
def check_existing_subscription(db: Session, company_id: int, tier_id: int) -> Optional[Subscription]:
    return db.query(Subscription).filter(
        Subscription.company_id == company_id,
        Subscription.tier_id == tier_id
    ).first()

def create_subscription(db: Session, subscription: SubscriptionCreate):
    # Validate the tier exists
    validate_tier(db, subscription.tier_id)

    # Check if company already has an active subscription for the tier
    existing_subscription = check_existing_subscription(db, subscription.company_id, subscription.tier_id)
    if existing_subscription:
        raise HTTPException(
            status_code=409,
            detail="Company already has an active subscription for this tier."
        )

    # Calculate valid_until date (1 year from created_at)
    valid_until = datetime.now() + datetime.timedelta(days=365)

    # Create the subscription
    db_subscription = Subscription(**subscription.dict(), valid_until=valid_until)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

# Retrieve all subscriptions with pagination and metadata
def get_subscriptions(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(Subscription).count()
    subscriptions = db.query(Subscription).offset(skip).limit(limit).all()
    return subscriptions

def get_subscription(db: Session, subscription_id: int):
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()

def update_subscription(db: Session, subscription_id: int, payload: SubscriptionUpdate):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription with ID {subscription_id} not found."
        )

    # If tier_id is provided, validate it exists
    if payload.tier_id:
        # Validate the new tier exists (similar to the create function)
        validate_tier(db, payload.tier_id)
        subscription.tier_id = payload.tier_id

    # Update transaction_code if provided
    if payload.transaction_code:
        subscription.transaction_code = payload.transaction_code
    
    # Update other fields as necessary (e.g., company_id is optional for updating)
    if payload.company_id:
        subscription.company_id = payload.company_id
    
    # Update any other fields here...
    try:
        db.commit()
        db.refresh(subscription)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update subscription: {str(e)}",
        )
    
    return subscription

def cancel_subscription(db: Session, subscription_id: int):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    
    subscription.status = "canceled"
    
    try:
        db.commit()
        db.refresh(subscription)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to cancel subscription: {str(e)}")
    
    return subscription
