from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.domain.md_vagas import vaga_controller
from app.domain.md_talentos import talento_controller
from app.domain.md_ia.model_loader import model_loader
from app.infra.database_migration import run_migrations

app = FastAPI(
    title="API de Análise de Talentos",
    description="Sistema para gerenciar vagas e ranquear talentos usando IA.",
    version="1.2.0"
)

# Adicione o middleware de CORS aqui
origins = [
    "http://localhost:5173",  # A URL do seu frontend Vite
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
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