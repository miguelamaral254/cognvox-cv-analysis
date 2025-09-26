from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from pydantic import BaseModel
from . import talento_service
from .talento_schema import TalentoCreate, TalentoPublic, ComentarioCreate, ComentarioPublic, TalentoStatusUpdate
from app.domain.md_users.user_schema import UserPublic
from app.domain.md_auth.auth_service import get_current_user

router = APIRouter(prefix="/talentos", tags=["Talentos"])

# Modelo Pydantic para o corpo da requisição do novo endpoint
class TalentoIdList(BaseModel):
    talento_ids: List[int]

@router.post("", response_model=TalentoPublic, status_code=status.HTTP_201_CREATED)
def inscrever_talento_endpoint(talento_data: TalentoCreate):
    novo_talento = talento_service.inscrever_novo_talento(talento_data.model_dump())
    return novo_talento

@router.get("", response_model=List[TalentoPublic])
def listar_talentos_endpoint(current_user: UserPublic = Depends(get_current_user)):
    return talento_service.listar_todos_talentos()

@router.get("/{talento_id}", response_model=TalentoPublic)
def buscar_talento_endpoint(talento_id: int, current_user: UserPublic = Depends(get_current_user)):
    return talento_service.buscar_talento_por_id(talento_id)

@router.get("/vaga/{vaga_id}", response_model=List[TalentoPublic])
def listar_talentos_por_vaga_endpoint(vaga_id: int, current_user: UserPublic = Depends(get_current_user)):
    return talento_service.listar_talentos_por_vaga(vaga_id)

@router.patch("/{talento_id}/status", response_model=TalentoPublic, tags=["Talentos"])
def update_talento_status_endpoint(
    talento_id: int,
    status_update: TalentoStatusUpdate,
    current_user: UserPublic = Depends(get_current_user)
):
    if current_user.role not in ["admin", "user1"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação não permitida.")
    return talento_service.update_talento_status(talento_id, status_update.ativo)

@router.post("/{talento_id}/comentarios", status_code=status.HTTP_204_NO_CONTENT) 
def create_comment_endpoint(
    talento_id: int,
    comentario_data: ComentarioCreate,
    current_user: UserPublic = Depends(get_current_user)
):
    talento_service.add_new_comment(
        texto=comentario_data.texto,
        talento_id=talento_id,
        user=current_user
    )
    return
@router.post("/comentarios/batch", response_model=List[ComentarioPublic], tags=["Comentários"])
def listar_comentarios_por_ids_endpoint(
    id_list: TalentoIdList,
    current_user: UserPublic = Depends(get_current_user)
):
    
    return talento_service.listar_comentarios_por_lista_de_talentos(id_list.talento_ids)

@router.delete("/comentarios/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comentários"])
def delete_comment_endpoint(
    comment_id: int,
    current_user: UserPublic = Depends(get_current_user)
):
    talento_service.remove_comment(comment_id, user=current_user)
    return