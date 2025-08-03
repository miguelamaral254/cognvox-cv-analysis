# app/domain/talentos/talento_controller.py
from fastapi import APIRouter, status
from . import talento_service
from .talento_schema import TalentoCreate, TalentoPublic, TalentoInList
from typing import List

router = APIRouter(prefix="/talentos", tags=["Talentos"])

@router.post("/", response_model=TalentoPublic, status_code=status.HTTP_201_CREATED)
def inscrever_talento_endpoint(talento_data: TalentoCreate):
    # Validação simples para garantir que a vaga existe poderia ser adicionada aqui
    novo_talento = talento_service.inscrever_novo_talento(talento_data.model_dump())
    return novo_talento

@router.get("/", response_model=List[TalentoInList])
def listar_talentos_endpoint():
    return talento_service.listar_todos_talentos()