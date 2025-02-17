from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt # type: ignore
from app.db import getDb
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.auth import SECRET_KEY, ALGORITHM

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT verification and fetch the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(getDb)) -> User:
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"Decoded payload: {payload}")  # Debugging: Check the decoded token payload
        
        user_id = payload.get("sub")  # Extract user ID from the token payload
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Fetch the user from the database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Debugging: Only print after ensuring the user is valid
        # print(f"User ID from token: {user_id}\nUser found in DB: {user}")
        # print(f"Authenticated User: {user}")  
        # print(f"User's Company ID: {user.company_id}") 

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Get Current logged-in user & enforce role-based access control
def get_current_user_with_role(*required_roles: str):
    def role_dependency(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(getDb)
    ) -> User:
        # Fetch the current user
        user = get_current_user(token, db)
        
        # Check for required roles
        if user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required one of: {', '.join(required_roles)}",
            )
        return user

    return role_dependency