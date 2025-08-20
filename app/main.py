from fastapi import FastAPI
from app.domain.md_vagas import vaga_controller
from app.domain.md_talentos import talento_controller
from app.domain.md_ia.model_loader import model_loader
from app.infra.database_migration import run_migrations

app = FastAPI(
    title="API de Análise de Talentos",
    description="Sistema para gerenciar vagas e ranquear talentos usando IA.",
    version="1.2.0"
)

@app.on_event("startup")
def startup_event():
    run_migrations()
    model_loader.get_model()

app.include_router(vaga_controller.router)
app.include_router(talento_controller.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Análise de Talentos!"}