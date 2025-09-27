from fastapi import HTTPException, status
from . import user_repository
from .user_schema import UserCreate, UserProfileUpdate, UserPasswordUpdate, UserStatusUpdate, RoleCreate, RoleUpdate
from app.domain.md_auth.password_utils import get_password_hash, verify_password

def create_new_user(user_data: UserCreate):
    existing_user = user_repository.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Um usuário com este e-mail já existe.")
    role = user_repository.find_role_by_id(user_data.user_role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A role com ID {user_data.user_role_id} não existe.")

    return user_repository.create_user(user_data)

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
def create_new_role(role_data: RoleCreate):
    existing_role = user_repository.find_role_by_name(role_data.nome)
    if existing_role:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma role com este nome já existe.")
    return user_repository.create_role(role_data)

def get_all_roles():
    return user_repository.find_all_roles()

def get_role_by_id(role_id: int):
    role = user_repository.find_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role não encontrada.")
    return role

def update_existing_role(role_id: int, role_data: RoleUpdate):
    get_role_by_id(role_id) # Garante que a role existe
    existing_role = user_repository.find_role_by_name(role_data.nome)
    if existing_role and existing_role['id'] != role_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma role com este nome já existe.")
    
    user_repository.update_role(role_id, role_data)
    return get_role_by_id(role_id)

def delete_role_by_id(role_id: int):
    get_role_by_id(role_id) 
    
    users_with_role = user_repository.count_users_by_role_id(role_id)
    if users_with_role > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível excluir a role, pois ela está em uso.")

    success = user_repository.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível excluir a role.")
    return {"message": "Role excluída com sucesso."}

# Adicione esta função ao final da seção de usuários no user_service.py

def update_user_role(user_id: int, new_role_name: str):
    get_user_by_id(user_id) # Garante que o usuário existe

    new_role = user_repository.find_role_by_name(new_role_name)
    if not new_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A role '{new_role_name}' não foi encontrada.")
    
    success = user_repository.update_role_for_user(user_id, new_role['id'])
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível atualizar a role do usuário.")

    return get_user_by_id(user_id)