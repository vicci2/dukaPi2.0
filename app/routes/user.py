from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate
from app.crud import user as crud_user
from app.db import getDb

users_router = APIRouter()

# POST /users/
@users_router.post("/", response_model=User,summary="Create a new user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(getDb)):
    return crud_user.create_user(db, user)

# GET /users/
@users_router.get("/", response_model=list[User],summary="Get a list of users")
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    return crud_user.get_users(db, skip=skip, limit=limit)

# GET /users/{user_id}
@users_router.get("/{user_id}", response_model=User,summary="Get a specific user by ID")
def get_user(user_id: int, db: Session = Depends(getDb)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
