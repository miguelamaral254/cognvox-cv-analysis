# app/domain/md_users/user_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER1 = "user1"
    USER2 = "user2"

class UserBase(BaseModel):
    nome: str = Field(..., example="Admin User")
    email: EmailStr = Field(..., example="admin@example.com")
    role: UserRole = Field(..., example=UserRole.ADMIN)

class UserCreate(UserBase):
    password: str = Field(..., example="uma_senha_forte")

class UserInDB(UserBase):
    hashed_password: str

class UserPublic(UserBase):
    id: int
    img_path: Optional[str] = None
    
    class Config:
        from_attributes = True