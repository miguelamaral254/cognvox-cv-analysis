from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.domain.md_vagas import vaga_controller
from app.domain.md_talentos import talento_controller
from app.domain.md_users import user_controller      
from app.domain.md_auth import auth_controller     
from app.domain.md_ia.model_loader import model_loader
from app.infra.database_migration import run_migrations

app = FastAPI(
    title="API de Análise de Talentos",
    description="Sistema para gerenciar vagas, talentos e usuários com autenticação JWT.",
    version="1.3.0"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    run_migrations()
    model_loader.get_model()

# Verifique se os routers de auth e users estão incluídos aqui
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(vaga_controller.router)
app.include_router(talento_controller.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Análise de Talentos!"}