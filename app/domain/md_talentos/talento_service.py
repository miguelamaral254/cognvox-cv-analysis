from fastapi import HTTPException, status
from mysql.connector.errors import IntegrityError  
from . import talento_repository, comentario_repository
from app.domain.md_vagas import vaga_repository
from app.domain.md_ia import ia_service
from app.domain.md_users.user_schema import UserPublic

def inscrever_novo_talento(talento_data: dict):
    vaga_id = talento_data.get("vaga_id")
    email = talento_data.get("email")

    if not vaga_repository.find_vaga_by_id(vaga_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A vaga com id={vaga_id} não foi encontrada."
        )

    if talento_repository.is_talento_already_applied(email=email, vaga_id=vaga_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Candidato já aplicou na vaga"
        )

    try:
        embedding = ia_service.gerar_embedding_para_talento(talento_data)
        talento_id = talento_repository.create_new_talento(talento_data, embedding)
        return talento_repository.find_talento_by_id(talento_id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este e-mail já está cadastrado para esta vaga.")
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro no serviço de IA: {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Não foi possível inscrever o talento. Erro: {e}")

def listar_todos_talentos():
    return talento_repository.find_all_talentos()

def buscar_talento_por_id(talento_id: int):
    talento = talento_repository.find_talento_by_id(talento_id)
    if not talento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talento não encontrado.")
    return talento

def listar_talentos_por_vaga(vaga_id: int):
    if not vaga_repository.find_vaga_by_id(vaga_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A vaga com id={vaga_id} não foi encontrada."
        )
    talentos = talento_repository.find_and_format_talentos_by_vaga_id(vaga_id)
    return talentos

def add_new_comment(texto: str, talento_id: int, user: UserPublic):
    talento = talento_repository.find_talento_by_id(talento_id)
    if not talento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talento não encontrado.")
    try:
        comentario_repository.create_comment(texto, talento_id, user.id)
        return 
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Não foi possível adicionar o comentário. Erro: {e}")
def listar_comentarios_por_lista_de_talentos(talento_ids: list[int]):
    if not talento_ids:
        return []
    return comentario_repository.find_comments_by_talento_ids(talento_ids)
def remove_comment(comment_id: int, user: UserPublic):
    comment = comentario_repository.find_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentário não encontrado.")
    if comment['user_id'] != user.id and user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para remover este comentário.")
    if not comentario_repository.delete_comment_by_id(comment_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível remover o comentário.")
    return True

def update_talento_status(talento_id: int, ativo: bool):
    talento = talento_repository.find_talento_by_id(talento_id)
    if not talento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talento não encontrado."
        )
    
    success = talento_repository.update_status(talento_id, ativo)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar o status do talento."
        )
    
    return talento_repository.find_talento_by_id(talento_id)

