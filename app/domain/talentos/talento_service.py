# app/domain/talentos/talento_service.py
from app.infra import repositories
from app.infra.ai_model import model_loader

def gerar_texto_para_embedding(talento_data: dict):
    exp_list = talento_data.get('experiencia_profissional') or []
    exp_textos = [f"Cargo: {exp.get('cargo', '')}. Descrição: {exp.get('descricao', '')}" for exp in exp_list]
    exp_completa = " ".join(exp_textos)
    
    return f"Sobre: {talento_data.get('sobre_mim', '')}. Formação: {talento_data.get('formacao', '')}. Experiências: {exp_completa}"

def inscrever_novo_talento(talento_data: dict):
    # Gerar embedding antes de salvar
    texto_completo = gerar_texto_para_embedding(talento_data)
    modelo_ia = model_loader.get_model()
    embedding = modelo_ia.encode(texto_completo).tolist()
    
    talento_id = repositories.create_new_talento(talento_data, embedding)
    return {"id": talento_id, **talento_data}

def listar_todos_talentos():
    return repositories.find_all_talentos()