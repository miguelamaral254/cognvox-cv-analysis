# app/domain/analysis/analysis_service.py
import pandas as pd
from sentence_transformers import util
from app.infra.ai_model import model_loader

def calcular_similaridade(df: pd.DataFrame, criterios: dict) -> pd.DataFrame:
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