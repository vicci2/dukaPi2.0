from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud import user as crud_user
from app.db import getDb

users_router = APIRouter()

# GET /users/
@users_router.get("/", response_model=list[User],summary="Get a list of users (Admin only)")
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    return crud_user.get_users(db, skip=skip, limit=limit)

# GET /users/{user_id}
@users_router.get("/{user_id}", response_model=User,summary="Get a specific user by ID")
def get_user(user_id: str, db: Session = Depends(getDb)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user (Admin or self)
@users_router.put(
    "/users/{user_id}",
    response_model=User,
    summary="Update user details (Admin or self)"
)
def update_user(user_id: str, payload: UserUpdate,db: Session = Depends(getDb)):
    return crud_user.update_user(db, user_id,)

# Update a user (Admin or self)
@users_router.delete(
    "/users/{user_id}",
    summary="Delete a user (Admin only)"
)
def delete_user(user_id: str,db: Session = Depends(getDb)):
    return crud_user.delete_user(db, user_id,)