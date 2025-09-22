from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Dict
from . import user_service
from .user_schema import UserCreate, UserPublic, UserProfileUpdate, UserPasswordUpdate, UserStatusUpdate
from app.domain.md_auth.auth_service import get_current_user

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_data: UserCreate, 
    current_user: UserPublic = Depends(get_current_user)
):
    return user_service.create_new_user(user_data)

@router.get("", response_model=List[UserPublic])
def list_users_endpoint(current_user: UserPublic = Depends(get_current_user)):
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=UserPublic)
def get_user_endpoint(
    user_id: int, 
    current_user: UserPublic = Depends(get_current_user)
):
    return user_service.get_user_by_id(user_id)

@router.put("/{user_id}/profile", response_model=UserPublic)
def update_profile_endpoint(
    user_id: int,
    profile_data: UserProfileUpdate,
    current_user: UserPublic = Depends(get_current_user)
):
    if user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação não permitida.")
    return user_service.update_user_profile(user_id, profile_data)

@router.put("/{user_id}/password", response_model=Dict[str, str])
def update_password_endpoint(
    user_id: int,
    password_data: UserPasswordUpdate,
    current_user: UserPublic = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação não permitida.")
    return user_service.update_user_password(user_id, password_data)

@router.put("/{user_id}/status", response_model=UserPublic)
def update_user_status_endpoint(
    user_id: int,
    status_data: UserStatusUpdate,
    current_user: UserPublic = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Ação não permitida. Apenas administradores podem alterar o status de um usuário."
        )
    return user_service.set_user_status(user_id, status_data)