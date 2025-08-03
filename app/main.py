# app/main.py
from fastapi import FastAPI
from app.domain.vagas import vaga_controller
from app.domain.talentos import talento_controller
from app.infra.ai_model import model_loader

app = FastAPI(
    title="API de Análise de Talentos",
    description="Sistema para gerenciar vagas e ranquear talentos usando IA.",
    version="1.1.0"
)

@app.on_event("startup")
def startup_event():
    model_loader.get_model()

app.include_router(vaga_controller.router)
app.include_router(talento_controller.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Análise de Talentos!"}