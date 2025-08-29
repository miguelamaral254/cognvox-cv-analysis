from fastapi import HTTPException, status
from psycopg2.errors import UniqueViolation
from . import talento_repository
from app.domain.md_vagas import vaga_repository
from app.domain.md_ia import ia_service

def inscrever_novo_talento(talento_data: dict):
    vaga_id = talento_data.get("vaga_id")
    if not vaga_repository.find_vaga_by_id(vaga_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A vaga com id={vaga_id} não foi encontrada."
        )

    try:
        embedding = ia_service.gerar_embedding_para_talento(talento_data)
        talento_id = talento_repository.create_new_talento(talento_data, embedding)
        novo_talento_criado = talento_repository.find_talento_by_id(talento_id)
        return novo_talento_criado
    
    except UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado para esta vaga."
        )
    except RuntimeError as e:
        # Erro específico se o modelo de IA não carregar
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro no serviço de IA: {e}"
        )
    except Exception as e:
        # Captura outros erros (ex: banco de dados) e os exibe
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não foi possível inscrever o talento. Erro: {e}"
        )
def listar_todos_talentos():
    return talento_repository.find_all_talentos()

def buscar_talento_por_id(talento_id: int):
    talento = talento_repository.find_talento_by_id(talento_id)
    if not talento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talento não encontrado."
        )
    return talento

def listar_talentos_por_vaga(vaga_id: int):
    if not vaga_repository.find_vaga_by_id(vaga_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A vaga com id={vaga_id} não foi encontrada."
        )
    
    talentos = talento_repository.find_and_format_talentos_by_vaga_id(vaga_id)
    return talentos