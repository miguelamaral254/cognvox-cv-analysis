from fastapi import HTTPException, status
from . import user_repository
from .user_schema import UserCreate

def create_new_user(user_data: UserCreate):
    existing_user = user_repository.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um usuário com este e-mail já existe."
        )
    
    try:
        new_user = user_repository.create_user(user_data)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não foi possível criar o usuário. Erro: {e}"
        )

def get_all_users():
    return user_repository.find_all_users()

def get_user_by_id(user_id: int):
    user = user_repository.find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    return user