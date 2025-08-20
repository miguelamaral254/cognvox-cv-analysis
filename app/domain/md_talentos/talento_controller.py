from fastapi import APIRouter, status
from . import talento_service
# A importação do TalentoInList não é mais necessária para este endpoint
from .talento_schema import TalentoCreate, TalentoPublic
from typing import List

router = APIRouter(prefix="/talentos", tags=["Talentos"])

@router.post("/", response_model=TalentoPublic, status_code=status.HTTP_201_CREATED)
def inscrever_talento_endpoint(talento_data: TalentoCreate):
    novo_talento = talento_service.inscrever_novo_talento(talento_data.model_dump())
    return novo_talento

# CORRIGIDO: O response_model agora é uma Lista do schema completo 'TalentoPublic'
@router.get("/", response_model=List[TalentoPublic])
def listar_talentos_endpoint():
    return talento_service.listar_todos_talentos()