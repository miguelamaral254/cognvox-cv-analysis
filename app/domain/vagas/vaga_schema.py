# app/domain/vagas/vaga_schema.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
 #TODO: Fazer descricao da vaga
# --- Modelos para Análise (Ranking) ---
class CandidatoRanqueado(BaseModel):
    id_talento: int
    nome: str
    email: str
    score_final: float
    scores_por_criterio: Dict[str, float]

class RankingResponse(BaseModel):
    titulo_vaga: str
    ranking: List[CandidatoRanqueado]

# --- Modelos para CRUD de Vagas ---
class VagaBase(BaseModel):
    titulo_vaga: str = Field(..., example="Desenvolvedor Python Sênior")
    criterios_de_analise: Dict[str, Any] = Field(..., example={
        "Experiencia": {"descricao": "Experiência com FastAPI e Pydantic", "colunas": ["sobre_mim"], "peso": 0.7}
    })
    top_x_candidatos: int = Field(..., example=10)

class VagaCreate(VagaBase):
    pass

class VagaPublic(VagaBase):
    id: int
    criado_em: datetime
    finalizada_em: datetime | None = None

    class Config:
        from_attributes = True

class VagaInList(BaseModel):
    id: int
    titulo_vaga: str
    criado_em: datetime
    finalizada_em: datetime | None = None