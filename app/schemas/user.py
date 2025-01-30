from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., example="John Doe")
    last_name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="johndoe@example.com")
    company_id: Optional[int] = Field(None, example=1)
    tel_no: str = Field(..., example="123-456-7890")
    avatar: Optional[str] = Field(None, example="https://example.com/avatar.jpg")

class UserCreate(UserBase):
    password: str = Field(..., example="SecurePassword123!")  

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, example="johnsmith")
    email: Optional[EmailStr] = Field(None, example="johnsmith@example.com")
    tel_no: str = Field(..., example="123-456-7890")
    firstName: Optional[str] = Field(None, example="John")
    lastName: Optional[str] = Field(None, example="Smith")
    avatar: Optional[str] = Field(None, example="https://example.com/new-avatar.jpg")
    role: Optional[str] = Field(None, example="manager")

    pass
class User(UserBase):
    id: str = Field(..., example=1)
    role: str = Field(..., example="user")  
    username: str = Field(..., example="username")  

    class Config:
        from_attributes = True  # Ensure SQLAlchemy model fields are included
         # Ensure password_hash is excluded from response
        exclude = {"password_hash"}
