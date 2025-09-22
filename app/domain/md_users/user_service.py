from fastapi import HTTPException, status
from . import user_repository
from .user_schema import UserCreate, UserProfileUpdate, UserPasswordUpdate, UserStatusUpdate
from app.domain.md_auth.password_utils import get_password_hash, verify_password

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

def update_user_profile(user_id: int, profile_data: UserProfileUpdate):
    user_to_update = get_user_by_id(user_id)

    if not verify_password(profile_data.currentPassword, user_to_update['hashed_password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha atual incorreta.")

    if profile_data.email != user_to_update['email']:
        existing_user = user_repository.get_user_by_email(profile_data.email)
        if existing_user and existing_user['id'] != user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este e-mail já está em uso.")
            
    success = user_repository.update_profile(user_id, profile_data)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível atualizar o perfil.")
    
    return get_user_by_id(user_id)

def update_user_password(user_id: int, password_data: UserPasswordUpdate):
    user = get_user_by_id(user_id)
    if not verify_password(password_data.currentPassword, user['hashed_password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha atual incorreta.")

    new_hashed_password = get_password_hash(password_data.newPassword)
    success = user_repository.update_password(user_id, new_hashed_password)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível alterar a senha.")
    
    return {"message": "Senha alterada com sucesso."}

def set_user_status(user_id: int, status_data: UserStatusUpdate):
    get_user_by_id(user_id)
    
    success = user_repository.set_user_active_status(user_id, status_data.is_active)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não foi possível atualizar o status do usuário."
        )
    
    return get_user_by_id(user_id)