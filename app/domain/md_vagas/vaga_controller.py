from fastapi import APIRouter, status, Depends
from typing import List
from . import vaga_service
from .vaga_schema import RankingResponse, VagaCreate, VagaPublic, AnaliseRequest, VagaFinalize
from app.domain.md_auth.auth_service import get_current_user
from .area_schema import AreaCreate, AreaPublic, AreaUpdate
from app.domain.md_users.user_schema import UserPublic 

router = APIRouter(prefix="/vagas", tags=["Vagas e Análise"])

@router.post("", response_model=VagaPublic, status_code=status.HTTP_201_CREATED)
def criar_vaga_endpoint(vaga_data: VagaCreate):
    return vaga_service.criar_nova_vaga(
        vaga_data.model_dump(exclude={'criado_por'}),
        criado_por=vaga_data.criado_por
    )

@router.get("", response_model=List[VagaPublic])
def listar_vagas_endpoint():
    return vaga_service.listar_vagas_abertas()

@router.post("/areas", response_model=AreaPublic, status_code=status.HTTP_201_CREATED, tags=["Áreas"])
def criar_area_endpoint(area_data: AreaCreate, _ = Depends(get_current_user)):
    return vaga_service.criar_nova_area(area_data.model_dump())

@router.get("/areas", response_model=List[AreaPublic], tags=["Áreas"])
def listar_areas_endpoint():
    return vaga_service.listar_todas_as_areas()

@router.get("/areas/{area_id}", response_model=AreaPublic, tags=["Áreas"])
def buscar_area_endpoint(area_id: int):
    return vaga_service.buscar_area_por_id(area_id)

@router.put("/areas/{area_id}", response_model=AreaPublic, tags=["Áreas"])
def atualizar_area_endpoint(area_id: int, area_data: AreaUpdate, _ = Depends(get_current_user)):
    return vaga_service.atualizar_area_existente(area_id, area_data.model_dump(exclude_unset=True))

@router.delete("/areas/{area_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Áreas"])
def deletar_area_endpoint(area_id: int, _ = Depends(get_current_user)):
    vaga_service.deletar_area_por_id(area_id)
    return None

@router.get("/{vaga_id}", response_model=VagaPublic)
def buscar_vaga_endpoint(vaga_id: int):
    return vaga_service.buscar_vaga_por_id(vaga_id)

@router.put("/{vaga_id}", response_model=VagaPublic)
def atualizar_vaga_endpoint(vaga_id: int, vaga_data: VagaCreate, _ = Depends(get_current_user)):
    return vaga_service.atualizar_vaga(vaga_id, vaga_data.model_dump())

@router.post("/{vaga_id}/finalizar", status_code=status.HTTP_204_NO_CONTENT)
def finalizar_vaga_endpoint(vaga_id: int, finalize_data: VagaFinalize):
    vaga_service.finalizar_vaga(vaga_id, finalizado_por=finalize_data.finalizado_por)
    return None

@router.post("/{vaga_id}/analisar", response_model=RankingResponse)
def analisar_vaga_endpoint(vaga_id: int, request_body: AnaliseRequest, _ = Depends(get_current_user)):
    return vaga_service.analisar_e_ranquear_vaga(vaga_id, request_body.top_candidatos)