from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.email.split('@')[0], 
        name=user.name,
        email=user.email,
        tel_no=user.tel_no,
        avatar=user.avatar,
        password_hash=user.password,
        role=UserRole.user,  # Default to "user" role
        company_id=user.company_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
