from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import getDb
from app.schemas.subscription import Subscription, SubscriptionCreate
from app.crud import subscription as crud_subscription

subscription_router = APIRouter()

@subscription_router.post(
    "/", 
    response_model=Subscription, 
    summary="Create a new subscription (Admin only)", 
    status_code=201
)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(getDb)):
    return crud_subscription.create_subscription(db, subscription)

@subscription_router.get(
    "/", 
    response_model=list[Subscription], 
    summary="Retrieve a list of subscriptions", 
    status_code=200
)
def get_subscriptions(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    return crud_subscription.get_subscriptions(db, skip=skip, limit=limit)

@subscription_router.get(
    "/{subscription_id}", 
    response_model=Subscription, 
    summary="Retrieve a specific subscription by ID", 
    status_code=200
)
def get_subscription(subscription_id: int, db: Session = Depends(getDb)):
    subscription = crud_subscription.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription
