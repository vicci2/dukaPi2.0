from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import getDb
from app.dependencies.auth import get_current_user_with_role
from app.schemas.subscription import SubscriptionCreate, SubscriptionRes, SubscriptionUpdate, cancelSubscription
from app.crud import subscription as crud_subscription
from app.schemas.user import User

subscription_router = APIRouter()

@subscription_router.post(
    "/", 
    response_model=SubscriptionRes, 
    summary="Create a new subscription (Admin only)", 
    status_code=201
)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(getDb)):
    return crud_subscription.create_subscription(db, subscription)

@subscription_router.get(
    "/", 
    response_model=list[SubscriptionRes], 
    summary="Retrieve a list of subscriptions", 
    status_code=200
)
def get_subscriptions(db: Session = Depends(getDb) ,current_user: User = Depends(get_current_user_with_role("admin"))):
    return crud_subscription.get_subscriptions(db, current_user)

@subscription_router.get(
    "/{subscription_id}", 
    response_model=SubscriptionUpdate, 
    summary="Retrieve a specific subscription by ID", 
    status_code=200
)
def get_subscription(subscription_id: int, db: Session = Depends(getDb),current_user: User = Depends(get_current_user_with_role("admin"))):
    subscription = crud_subscription.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@subscription_router.put(
    "/{subscription_id}",
    response_model=SubscriptionUpdate,
    summary="Update a subscription (Admin only)",
    status_code=200,
)
def update_subscription(subscription_id: int, payload: SubscriptionUpdate, db: Session = Depends(getDb),current_user: User = Depends(get_current_user_with_role("admin", "manager"))
):
    """
    Update a subscription by ID. You can update the tier, transaction code, and other optional fields.
    """
    updated_subscription = crud_subscription.update_subscription(db, subscription_id, payload)
    return updated_subscription

@subscription_router.put(
    "/{subscription_id}/cancel",
    response_model=cancelSubscription,
    summary="Cancel a subscription (Admin only)",
    status_code=200,
)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(getDb)
    ,current_user: User = Depends(get_current_user_with_role("admin"))
):
    """
    Mark a subscription as canceled without deleting it. 
    This ensures that subscription history is kept intact.
    """
    canceled_subscription = crud_subscription.cancel_subscription(db, subscription_id)
    return canceled_subscription
