from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class ModeloTrabalho(str, Enum):
    REMOTO = "Remoto"
    HIBRIDO = "Híbrido"
    PRESENCIAL = "Presencial"

class AnaliseRequest(BaseModel):
    top_candidatos: int = Field(10, ge=1, description="O número de candidatos no ranking final.")

class CandidatoRanqueado(BaseModel):
    id_talento: int
    nome: str
    email: str
    score_final: float
    scores_por_criterio: Dict[str, float]

class RankingResponse(BaseModel):
    titulo_vaga: str
    ranking: List[CandidatoRanqueado]

class VagaBase(BaseModel):
    titulo_vaga: str = Field(..., example="Desenvolvedor Python Sênior")
    descricao: str = Field(..., example="Estamos procurando um desenvolvedor Python para atuar...")
    cidade: str = Field(..., example="Recife")
    modelo_trabalho: ModeloTrabalho = Field(..., example=ModeloTrabalho.HIBRIDO)
    area_id: int = Field(..., example=1) 
    criterios_de_analise: Dict[str, Any] = Field(..., example={
        "Experiencia": {"descricao": "Experiência com FastAPI...", "colunas": ["sobre_mim"], "peso": 0.7}
    })
    vaga_pcd: bool = Field(False, description="Indica se a vaga é afirmativa para Pessoas com Deficiência (PCD).")
    criterios_diferenciais_de_analise: Optional[Dict[str, Any]] = Field(None, example={
        "Inglês Avançado": {"descricao": "Comunicação em inglês será um diferencial", "colunas": ["idiomas"], "peso": 0.1}
    })

class VagaCreate(VagaBase):
    criado_por: int = Field(..., example=1, description="ID do usuário que está criando a vaga.")


class VagaPublic(VagaBase):
    id: int
    criado_em: datetime
    finalizada_em: Optional[datetime] = None
    nome_area: Optional[str] = None
    criado_por: Optional[int] = None
    finalizado_por: Optional[int] = None


    class Config:
        from_attributes = True

class VagaInList(BaseModel):
    id: int
    titulo_vaga: str
    descricao: str
    cidade: str 
    modelo_trabalho: ModeloTrabalho
    area_id: int
    nome_area: Optional[str] = None
    vaga_pcd: bool = Field(False)
    criado_em: datetime
    finalizada_em: Optional[datetime] = None
class VagaFinalize(BaseModel):
    finalizado_por: int = Field(..., example=1, description="ID do usuário que está finalizando a vaga.")
