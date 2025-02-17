from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db import Base
import uuid

# Enum for user roles
class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    staff = "staff"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  
    company_id = Column(Integer, ForeignKey("companies.id"))
    fullName = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    tel_no = Column(String, nullable=False, unique=True)
    avatar = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user) 
    last_login = Column(DateTime(timezone=False), server_default=func.now()) 
    created_at = Column(DateTime(timezone=False), server_default=func.now())  

    company = relationship("Company", back_populates="user")
