from fastapi import APIRouter, HTTPException, status
from app.domain.md_users import user_repository
from . import auth_service
from .auth_schema import Token, AuthRequest

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/token", response_model=Token)
def login_for_access_token(auth_data: AuthRequest):
    user = user_repository.get_user_by_email(auth_data.email)

    if not user or not auth_service.verify_password(auth_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get('is_active', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo, contate a administração"
        )
    
    token_data = {
        "sub": user['email'],
        "id": user['id'],
        "nome": user['nome'],
        "role": user['role']
    }
    
    access_token = auth_service.create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}