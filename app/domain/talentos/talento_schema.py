# app/domain/talentos/talento_schema.py
from pydantic import BaseModel, Field, EmailStr
from typing import List, Any, Dict
from datetime import datetime

class TalentoBase(BaseModel):
    nome: str = Field(..., example="Maria Silva")
    email: EmailStr = Field(..., example="maria.silva@example.com")
    sobre_mim: str | None = Field(None, example="Sou uma desenvolvedora apaixonada por tecnologia...")
    experiencia_profissional: List[Dict[str, Any]] | None = Field(None, example=[{"cargo": "Dev Pleno", "empresa": "Tech Corp"}])
    formacao: str | None = Field(None, example="Ciência da Computação - USP")
    aceita_termos: bool

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