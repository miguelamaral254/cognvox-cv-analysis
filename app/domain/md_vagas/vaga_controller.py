from fastapi import APIRouter, status, Depends
from typing import List
from . import vaga_service
from .vaga_schema import RankingResponse, VagaCreate, VagaPublic, AnaliseRequest
from app.domain.md_auth.auth_service import get_current_user

router = APIRouter(prefix="/vagas", tags=["Vagas e Análise"])

@router.post("", response_model=VagaPublic, status_code=status.HTTP_201_CREATED)
def criar_vaga_endpoint(vaga_data: VagaCreate, _ = Depends(get_current_user)):
    return vaga_service.criar_nova_vaga(vaga_data.model_dump())

@router.get("", response_model=List[VagaPublic])
def listar_vagas_endpoint(_ = Depends(get_current_user)):
    return vaga_service.listar_vagas_abertas()

@router.get("/{vaga_id}", response_model=VagaPublic)
def buscar_vaga_endpoint(vaga_id: int, _ = Depends(get_current_user)):
    return vaga_service.buscar_vaga_por_id(vaga_id)

@router.put("/{vaga_id}", response_model=VagaPublic)
def atualizar_vaga_endpoint(vaga_id: int, vaga_data: VagaCreate, _ = Depends(get_current_user)):
    return vaga_service.atualizar_vaga(vaga_id, vaga_data.model_dump())

@router.post("/{vaga_id}/finalizar", status_code=status.HTTP_204_NO_CONTENT)
def finalizar_vaga_endpoint(vaga_id: int, _ = Depends(get_current_user)):
    vaga_service.finalizar_vaga(vaga_id)
    return None 

@router.post("/{vaga_id}/analisar", response_model=RankingResponse)
def analisar_vaga_endpoint(vaga_id: int, request_body: AnaliseRequest, _ = Depends(get_current_user)):
    return vaga_service.analisar_e_ranquear_vaga(vaga_id, request_body.top_candidatos)