from fastapi import APIRouter, Form, Depends
from sqlalchemy.orm import Session
from app.db import getDb
from app.dependencies.auth import get_current_user, get_current_user_with_role
from app.models.user import User
from app.schemas.user import User
from app.crud import auth as crud_auth
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
# from app.utils.methods_utils import log_audit_event

# Auth Router
auth_router = APIRouter()

# Registration Endpoint
@auth_router.post("/register", status_code=201)
def register_user(payload: RegisterRequest, db: Session = Depends(getDb)):
    return crud_auth.create_user(db, payload)

# Login Endpoint
@auth_router.post("/login", response_model=TokenResponse)
def login_user(
    # username: str = Form(..., example="doe_joe"),
    # password: str = Form(..., example="joe@Doe"),
    payload: LoginRequest, 
    db: Session = Depends(getDb)
):
  return crud_auth.login_user(db, payload.username, payload.password)

# @auth_router.get("/me")
# def get_me(current_user: User = Depends(get_current_user)):
#     return {"user_id": current_user.id, "username": current_user.username, "role": current_user.role}

# @auth_router.get("/admin")
# def admin_only(current_user: User = Depends(get_current_user_with_role("admin"))):
#     return {"message": "Welcome, admin!"}