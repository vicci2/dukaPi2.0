from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user_with_role
from app.schemas.user import User, UserUpdate
from app.crud import user as crud_user
from app.db import getDb

users_router = APIRouter()

# GET /users/
@users_router.get("/", response_model=list[User],summary="Get a list of users (Admin only)")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    return crud_user.get_users(db, current_user)

# GET /users/{user_id}
@users_router.get("/{user_id}", response_model=User,summary="Get a specific user by ID")
def get_user(user_id: str, db: Session = Depends(getDb),current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    user = crud_user.get_user(db, user_id, current_user)
    return user

# Update a user (Admin or self)
@users_router.put(
    "/users/{user_id}",
    response_model=User,
    summary="Update user details (Admin or self)"
)
def update_user(user_id: str, payload: UserUpdate,db: Session = Depends(getDb), current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    return crud_user.update_user(db, user_id, payload, current_user)

# Update a user (Admin or self)
@users_router.delete(
    "/users/{user_id}",
    summary="Delete a user (Admin only)"
)
def delete_user(user_id: str,db: Session = Depends(getDb),current_user: User = Depends(get_current_user_with_role("admin", "manager"))):
    return crud_user.delete_user(db, user_id, current_user)