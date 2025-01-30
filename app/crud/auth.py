from fastapi import Form, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, TokenResponse
from app.utils.auth import create_access_token, hash_password, verify_password

def create_user(db: Session, user: RegisterRequest):
    """
    Register a new user and log the event.
    """
    existing_user = db.query(User).filter((User.username == user.email.split('@')[0]) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered."
        )
    try:
        hashed_password = hash_password(user.password)
        
        new_user = User(
            name=user.name,
            last_name=user.last_name,
            username=user.email.split('@')[0], 
            email=user.email,
            tel_no=user.tel_no,
            avatar=user.avatar,
            password_hash=hashed_password,
            role=UserRole.user,  # Default to "user" role
            company_id=user.company_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Log successful registration
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )
    return {"message": "User registered successfully", "user_id": new_user.id}

def login_user(db: Session, username: str = Form(..., example="doe_joe"),
    password: str = Form(..., example="joe@Doe"),
            #    ,user: TokenResponse
            ):
    """
    Authenticate a user, generate an access token, and log the event.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        # Log failed login attempt

        # Raise an HTTP exception with a generic error message
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        # Generate an access token for the authenticated user
        access_token = create_access_token({"sub": user.id, "role": user.role})

        # print(f"Generated Token: {access_token}")

        # Log successful login

        # Return the access token
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        # Log the exception if token generation fails

        # Raise a server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the access token.",
        )
    
    