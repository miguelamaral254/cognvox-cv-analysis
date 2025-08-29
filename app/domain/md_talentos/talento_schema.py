from pydantic import BaseModel, Field, EmailStr
from typing import List, Any, Dict
from datetime import datetime

class TalentoBase(BaseModel):
    nome: str = Field(..., max_length=255, example="Maria Silva")
    email: EmailStr = Field(..., example="maria.silva@example.com")
    cidade: str | None = Field(None, max_length=100, example="Recife")
    telefone: str | None = Field(None, max_length=20, example="+55 11 98765-4321")
    sobre_mim: str | None = Field(None, example="Sou uma desenvolvedora apaixonada por tecnologia...")
    
    experiencia_profissional: List[Dict[str, Any]] | None = None
    formacao: List[Dict[str, Any]] | None = None
    idiomas: List[Dict[str, Any]] | None = None
    cursos_extracurriculares: List[Dict[str, Any]] | None = None
    redes_sociais: List[Dict[str, Any]] | None = None
    deficiencia_detalhes: List[Dict[str, Any]] | None = None

    respostas_criterios: Dict[str, str] | None = None
    respostas_diferenciais: Dict[str, str] | None = None
    
    deficiencia: bool = Field(False)
    aceita_termos: bool
    confirmar_dados_verdadeiros: bool

class TalentoCreate(TalentoBase):
    vaga_id: int

class TalentoPublic(TalentoBase):
    id: int
    vaga_id: int
    criado_em: datetime

class TalentoInList(BaseModel):
    id: int
    nome: str
    email: EmailStr
    vaga_id: int
    cidade: str | None = None
