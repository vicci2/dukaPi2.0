from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: EmailStr = Field(..., example="johndoe@example.com")
    company_id: int = Field(..., example=1)
    password: str = Field(..., example="securePassword123")
    tel_no: str = Field(..., example="123-456-7890")
    avatar: Optional[str] = Field(None, example="https://example.com/avatar.jpg")

class LoginRequest(BaseModel):
    username: str = Field(..., example="doe_joe")
    password: str = Field(..., example="joe@Doe")

class TokenResponse(BaseModel):
    access_token: str = Field(..., example="Acess token")
    token_type: str = Field(..., example="Token Type")