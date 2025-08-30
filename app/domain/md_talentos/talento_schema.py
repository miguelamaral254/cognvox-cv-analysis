from pydantic import BaseModel, Field, EmailStr
from typing import List, Any, Dict
from datetime import datetime

class ComentarioBase(BaseModel):
    texto: str = Field(..., example="Candidato parece promissor.")

class ComentarioCreate(ComentarioBase):
    pass 

class ComentarioPublic(ComentarioBase):
    id: int
    criado_em: datetime
    user_id: int
    user_nome: str

    class Config:
        from_attributes = True

class TalentoStatusUpdate(BaseModel):
    ativo: bool

class TalentoBase(BaseModel):
    nome: str = Field(..., max_length=255, example="Maria Silva")
    email: EmailStr = Field(..., example="maria.silva@example.com")
    cidade: str | None = Field(None, max_length=100, example="Recife")
    telefone: str | None = Field(None, max_length=20, example="+55 11 98765-4321")
    sobre_mim: str | None = Field(None, example="Sou uma desenvolvedora apaixonada por tecnologia...")
    
    experiencia_profissional: List[Dict[str, Any]] | None = Field(None, example=[{"cargo": "Dev Pleno", "empresa": "Tech Corp"}])
    formacao: List[Dict[str, Any]] | None = Field(None, example=[{"instituicao": "USP", "curso": "Ciência da Computação"}])
    idiomas: List[Dict[str, Any]] | None = Field(None, example=[{"idioma": "Inglês", "nivel": "Avançado"}])
    cursos_extracurriculares: List[Dict[str, Any]] | None = Field(None, example=[{"curso": "Cloud AWS", "instituicao": "Online School"}])
    redes_sociais: List[Dict[str, Any]] | None = Field(None, example=[{"rede": "LinkedIn", "url": "https://linkedin.com/in/..."}])
    deficiencia_detalhes: List[Dict[str, Any]] | None = Field(None, example=[{"tipo": "Visual", "descricao": "Necessita de leitor de tela", "cid": "H54.1"}])

    respostas_criterios: Dict[str, str] | None = Field(None, example={"Experiencia_Tecnica": "Tenho 5 anos de experiência com..."})
    respostas_diferenciais: Dict[str, str] | None = Field(None, example={"Ingles_Avancado": "Possuo certificação TOEFL."})
    
    deficiencia: bool = Field(False)
    aceita_termos: bool
    confirmar_dados_verdadeiros: bool
    ativo: bool = Field(True)

class TalentoCreate(TalentoBase):
    vaga_id: int

class TalentoPublic(TalentoBase):
    id: int
    vaga_id: int
    criado_em: datetime
    area_id: int | None = None
    nome_area: str | None = None
    comentarios: List[ComentarioPublic] = []

class TalentoInList(BaseModel):
    id: int
    nome: str
    email: EmailStr
    vaga_id: int
    cidade: str | None = None
    area_id: int | None = None
    nome_area: str | None = None
    ativo: bool