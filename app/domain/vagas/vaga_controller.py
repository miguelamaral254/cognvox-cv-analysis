from fastapi import APIRouter, HTTPException, status
from . import vaga_service
from .vaga_schema import RankingResponse, VagaCreate, VagaPublic, VagaInList
from typing import List

router = APIRouter(prefix="/vagas", tags=["Vagas e Análise"])

@router.post("/", response_model=VagaPublic, status_code=status.HTTP_201_CREATED)
def criar_vaga_endpoint(vaga_data: VagaCreate):
    vaga = vaga_service.criar_nova_vaga(vaga_data.model_dump())
    return vaga

@router.get("", response_model=List[VagaInList])
def listar_vagas_endpoint():
    return vaga_service.listar_vagas_abertas()

@router.get("/{vaga_id}", response_model=VagaPublic)
def buscar_vaga_endpoint(vaga_id: int):
    vaga = vaga_service.buscar_vaga_por_id(vaga_id)
    if not vaga: raise HTTPException(status.HTTP_404_NOT_FOUND, "Vaga não encontrada.")
    return vaga

@router.put("/{vaga_id}", response_model=VagaPublic)
def atualizar_vaga_endpoint(vaga_id: int, vaga_data: VagaCreate):
    vaga = vaga_service.atualizar_vaga(vaga_id, vaga_data.model_dump())
    if not vaga: raise HTTPException(status.HTTP_404_NOT_FOUND, "Vaga não encontrada para atualizar.")
    return vaga

@router.post("/{vaga_id}/finalizar", response_model=VagaPublic)
def finalizar_vaga_endpoint(vaga_id: int):
    vaga = vaga_service.finalizar_vaga(vaga_id)
    if not vaga: raise HTTPException(status.HTTP_404_NOT_FOUND, "Vaga não encontrada para finalizar.")
    return vaga

@router.post("/{vaga_id}/analisar", response_model=RankingResponse)
def analisar_vaga_endpoint(vaga_id: int):
    resultado = vaga_service.analisar_e_ranquear_vaga(vaga_id)
    if resultado is None: raise HTTPException(status.HTTP_404_NOT_FOUND, "Vaga não encontrada ou já foi finalizada.")
    return resultado