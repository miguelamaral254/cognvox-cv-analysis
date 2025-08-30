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

class UserProfileUpdate(BaseModel):
    nome: str = Field(..., example="Novo Nome do Usuário")
    email: EmailStr = Field(..., example="novo.email@example.com")
    currentPassword: str = Field(..., description="Senha atual do usuário para confirmação")


class UserPasswordUpdate(BaseModel):
    currentPassword: str = Field(..., example="senha_atual_123")
    newPassword: str = Field(..., min_length=8, example="nova_senha_forte_456")