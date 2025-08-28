from fastapi import APIRouter, status, Depends
from typing import List
from . import user_service
from .user_schema import UserCreate, UserPublic
from app.domain.md_auth.auth_service import get_current_user

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_data: UserCreate, 
    current_user: UserPublic = Depends(get_current_user)
):
    new_user = user_service.create_new_user(user_data)
    return new_user

@router.get("", response_model=List[UserPublic])
def list_users_endpoint(current_user: UserPublic = Depends(get_current_user)):
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=UserPublic)
def get_user_endpoint(
    user_id: int, 
    current_user: UserPublic = Depends(get_current_user)
):
    return user_service.get_user_by_id(user_id)