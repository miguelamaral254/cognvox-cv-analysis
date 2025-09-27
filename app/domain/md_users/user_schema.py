from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# --- Schemas para Roles ---
class RoleBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50, example="recrutador_senior")

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

# --- Schemas para Usuários ---
class UserBase(BaseModel):
    nome: str = Field(..., example="Admin User")
    email: EmailStr = Field(..., example="admin@example.com")
    role: Optional[str] = Field(None, example="admin")
    is_active: bool = Field(True, example=True)

class UserCreate(BaseModel):
    nome: str = Field(..., example="Novo Usuário")
    email: EmailStr = Field(..., example="novo.usuario@example.com")
    password: str = Field(..., example="uma_senha_forte")
    user_role_id: int = Field(..., example=2, description="ID da role do usuário")

class UserPublic(UserBase):
    id: int
    img_path: Optional[str] = None
    user_role_id: int
    
    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    nome: str = Field(..., example="Novo Nome do Usuário")
    email: EmailStr = Field(..., example="novo.email@example.com")
    currentPassword: str = Field(..., description="Senha atual do usuário para confirmação")

class UserPasswordUpdate(BaseModel):
    currentPassword: str = Field(..., example="senha_atual_123")
    newPassword: str = Field(..., min_length=8, example="nova_senha_forte_456")

class UserStatusUpdate(BaseModel):
    is_active: bool
class UserRoleUpdate(BaseModel):
    role: str = Field(..., example="recrutador")