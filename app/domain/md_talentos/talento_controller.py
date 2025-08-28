from fastapi import APIRouter, status, Depends
from typing import List
from . import talento_service
from .talento_schema import TalentoCreate, TalentoPublic
from app.domain.md_auth.auth_service import get_current_user
from app.domain.md_users.user_schema import UserPublic

router = APIRouter(prefix="/talentos", tags=["Talentos"])

@router.post("", response_model=TalentoPublic, status_code=status.HTTP_201_CREATED)
def inscrever_talento_endpoint(talento_data: TalentoCreate):
    novo_talento = talento_service.inscrever_novo_talento(talento_data.model_dump())
    return novo_talento

@router.get("", response_model=List[TalentoPublic])
def listar_talentos_endpoint(_ = Depends(get_current_user)):
    return talento_service.listar_todos_talentos()

@router.get("/{talento_id}", response_model=TalentoPublic)
def buscar_talento_endpoint(talento_id: int, _ = Depends(get_current_user)):
    return talento_service.buscar_talento_por_id(talento_id)