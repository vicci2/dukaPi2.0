from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate, User as useres

def get_users(db: Session, current_user) -> list[useres]:
    users = db.query(User).filter(User.company_id == current_user.company_id).offset(0).limit(100).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    return users

def get_user(db: Session, user_id: str, current_user):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    
    if current_user and str(user.id) != str(current_user.id):  
        raise HTTPException(status_code=403, detail="Not authorized to access this profile")

    return user

def update_user(db: Session, user_id: str, payload: UserUpdate, current_user):
    """
    Update user details.
    """
    # Log failure if unauthorized update attempt
    user = get_user(db, user_id, current_user)
    # Log failure if user not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    try:
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()

        # Log the failed transaction
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )

    return user

def delete_user(db: Session, user_id: str, current_user):
    """
    Delete a User
    """
    if str(user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    user = get_user(db, user_id, current_user)
    # Log failure if unauthorized update attempt
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )

    return {"message": f"User with ID {user_id} has been deleted successfully."}

