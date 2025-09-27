from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AreaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, example="Tecnologia")
    descricao: Optional[str] = Field(None, example="Área destinada a vagas de desenvolvimento, infraestrutura e inovação.")

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100, example="Tecnologia e Inovação")
    descricao: Optional[str] = Field(None, example="Descrição atualizada da área.")

class AreaPublic(AreaBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True