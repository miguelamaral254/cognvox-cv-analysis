import pandas as pd
from sentence_transformers import util
from .model_loader import model_loader

def calcular_similaridade(df: pd.DataFrame, criterios: dict) -> pd.DataFrame:
    modelo_ia = model_loader.get_model()
    if modelo_ia is None:
        raise RuntimeError("Modelo de IA não foi carregado.")

    LIMITE_CONFIANCA_RESPOSTA = 0.35

    for nome_criterio, detalhes in criterios.items():
        print(f"   - Analisando critério: '{nome_criterio}'...")

        peso_resposta_especifica = detalhes.get("peso_resposta", 0.7)
        peso_texto_geral = detalhes.get("peso_geral", 0.3)
        
        respostas_especificas = df['respostas_criterios'].apply(
            lambda r: r.get(nome_criterio, "") if isinstance(r, dict) else ""
        )

        mascara_nao_possui = (respostas_especificas == "Não possui o critério")
        df[f'similaridade_{nome_criterio}'] = 0.0
        df_para_analisar = df[~mascara_nao_possui]

        if not df_para_analisar.empty:
            descricao_criterio = detalhes["descricao"]
            colunas_gerais = detalhes["colunas"]
            
            textos_gerais_combinados = df_para_analisar[colunas_gerais].astype(str).fillna('').agg(' '.join, axis=1)
            respostas_para_analisar = respostas_especificas[~mascara_nao_possui]

            embedding_criterio = modelo_ia.encode(descricao_criterio, convert_to_tensor=True)
            embeddings_gerais = modelo_ia.encode(textos_gerais_combinados.tolist(), convert_to_tensor=True)
            embeddings_especificos = modelo_ia.encode(respostas_para_analisar.tolist(), convert_to_tensor=True)
            
            similaridades_gerais = util.cos_sim(embedding_criterio, embeddings_gerais)[0]
            similaridades_especificas = util.cos_sim(embedding_criterio, embeddings_especificos)[0]
            
            similaridade_final_ajustada = []
            for i in range(len(df_para_analisar)):
                score_especifico = similaridades_especificas[i]
                score_geral = similaridades_gerais[i]

                if score_especifico < LIMITE_CONFIANCA_RESPOSTA:
                    score_geral_penalizado = score_geral * score_especifico
                else:
                    score_geral_penalizado = score_geral

                score_final_criterio = (score_especifico * peso_resposta_especifica) + (score_geral_penalizado * peso_texto_geral)
                similaridade_final_ajustada.append(score_final_criterio)

            df.loc[~mascara_nao_possui, f'similaridade_{nome_criterio}'] = [s.item() for s in similaridade_final_ajustada]
            
    return df

def gerar_embedding_para_talento(talento_data: dict) -> list:
    def format_json_field(data, key):
        items = data.get(key) or []
        return " ".join([str(item) for item in items])

    exp_completa = format_json_field(talento_data, 'experiencia_profissional')
    formacao_completa = format_json_field(talento_data, 'formacao')
    cursos_completos = format_json_field(talento_data, 'cursos_extracurriculares')
    idiomas_completos = format_json_field(talento_data, 'idiomas')
    
    texto_completo = (
        f"Sobre: {talento_data.get('sobre_mim', '')}. "
        f"Formação: {formacao_completa}. "
        f"Cursos: {cursos_completos}. "
        f"Experiências: {exp_completa}. "
        f"Idiomas: {idiomas_completos}."
    )

    modelo_ia = model_loader.get_model()
    embedding = modelo_ia.encode(texto_completo).tolist()
    return embedding