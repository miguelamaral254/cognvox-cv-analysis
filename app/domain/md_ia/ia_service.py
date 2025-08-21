import pandas as pd
from sentence_transformers import util
from .model_loader import model_loader

def calcular_similaridade(df: pd.DataFrame, criterios: dict) -> pd.DataFrame:
    """
    Calcula a similaridade de cosseno entre os textos dos candidatos e as descrições dos critérios.
    """
    modelo_ia = model_loader.get_model()
    if modelo_ia is None:
        raise RuntimeError("Modelo de IA não foi carregado.")

    for nome_criterio, detalhes in criterios.items():
        print(f"   - Analisando critério: '{nome_criterio}'...")
        
        descricao = detalhes["descricao"]
        colunas = detalhes["colunas"]
        
        textos_combinados = df[colunas].astype(str).fillna('').agg(' '.join, axis=1)
        
        embedding_alvo = modelo_ia.encode(descricao, convert_to_tensor=True)
        embeddings_candidatos = modelo_ia.encode(textos_combinados.tolist(), convert_to_tensor=True)
        
        similaridades = util.cos_sim(embedding_alvo, embeddings_candidatos)
        df[f'similaridade_{nome_criterio}'] = similaridades[0].cpu().numpy()
        
    return df

def gerar_embedding_para_talento(talento_data: dict) -> list:
    """
    Gera um vetor de embedding para os dados de um novo talento.
    """
    # Combina os campos de texto relevantes do talento
    exp_list = talento_data.get('experiencia_profissional') or []
    exp_textos = [f"Cargo: {exp.get('cargo', '')}. Descrição: {exp.get('descricao', '')}" for exp in exp_list]
    exp_completa = " ".join(exp_textos)
    
    texto_completo = f"Sobre: {talento_data.get('sobre_mim', '')}. Formação: {talento_data.get('formacao', '')}. Experiências: {exp_completa}"

    # Gera e retorna o embedding
    modelo_ia = model_loader.get_model()
    embedding = modelo_ia.encode(texto_completo).tolist()
    return embedding