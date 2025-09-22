from fastapi import APIRouter, HTTPException, status
from app.domain.md_users import user_repository
from . import auth_service
from .auth_schema import Token, AuthRequest

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/token", response_model=Token)
def login_for_access_token(auth_data: AuthRequest):
    # --- INÍCIO DA DEPURAÇÃO ---
    print("\n--- DEBUG LOGIN ---")
    print(f"1. Tentativa de login para o email: '{auth_data.email}'")

    user = user_repository.get_user_by_email(auth_data.email)

    if not user:
        print("2. RESULTADO: Usuário NÃO encontrado no banco de dados.")
        print("--- FIM DO DEBUG ---\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"2. RESULTADO: Usuário encontrado no banco. ID: {user.get('id')}")
    print(f"3. Senha recebida na API (texto plano): '{auth_data.password}'")
    print(f"4. Hash da senha vindo do banco: '{user.get('hashed_password')}'")

    is_password_correct = auth_service.verify_password(auth_data.password, user['hashed_password'])
    
    print(f"5. Resultado da verificação (passlib.verify): {is_password_correct}")
    print("--- FIM DO DEBUG ---\n")
    # --- FIM DA DEPURAÇÃO ---

    if not is_password_correct:
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