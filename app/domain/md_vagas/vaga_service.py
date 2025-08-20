from fastapi import HTTPException, status
from . import vaga_repository
from app.domain.md_talentos import talento_repository
from app.domain.md_ia import ia_service

def formatar_experiencia(exp_json):
    if not exp_json or not isinstance(exp_json, list): return ""
    textos = [f"Cargo: {exp.get('cargo', '')}. Descrição: {exp.get('descricao', '')}" for exp in exp_json]
    return " ".join(textos)

def analisar_e_ranquear_vaga(vaga_id: int):
    params_vaga = vaga_repository.find_vaga_by_id(vaga_id)
    if not params_vaga or params_vaga.get("finalizada_em"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaga não encontrada ou já foi finalizada."
        )
    
    df_candidatos = talento_repository.find_talentos_by_vaga_id(vaga_id)
    if df_candidatos.empty: 
        return {"titulo_vaga": params_vaga["titulo_vaga"], "ranking": []}

    if 'experiencia_profissional' in df_candidatos.columns:
        df_candidatos['experiencia_formatada'] = df_candidatos['experiencia_profissional'].apply(formatar_experiencia)

    criterios = params_vaga["criterios_de_analise"]
    df_analisado = ia_service.calcular_similaridade(df_candidatos, criterios)

    df_analisado['score_final'] = 0.0
    for nome, detalhes in criterios.items():
        df_analisado['score_final'] += df_analisado[f'similaridade_{nome}'] * float(detalhes.get("peso", 1.0))

    df_ranqueado = df_analisado.sort_values(by='score_final', ascending=False)
    top_candidatos = df_ranqueado.head(params_vaga["top_x_candidatos"])
    
    ranking_para_salvar, ranking_para_resposta = [], []
    for _, row in top_candidatos.iterrows():
        scores_detalhados = {nome: row[f'similaridade_{nome}'] for nome in criterios.keys()}
        ranking_para_salvar.append({"id": row['id'], "score_final": row['score_final'], "scores_detalhados": scores_detalhados})
        ranking_para_resposta.append({
            "id_talento": row['id'], "nome": row['nome'], "email": row['email'],
            "score_final": round(row['score_final'] * 100, 2),
            "scores_por_criterio": {nome: round(score * 100, 2) for nome, score in scores_detalhados.items()}
        })
    
    vaga_repository.save_ranking(vaga_id, ranking_para_salvar)
    return {"titulo_vaga": params_vaga["titulo_vaga"], "ranking": ranking_para_resposta}

def criar_nova_vaga(vaga_data: dict):
    try:
        vaga_id = vaga_repository.create_new_vaga(vaga_data)
        return vaga_repository.find_vaga_by_id(vaga_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não foi possível criar a vaga. Verifique os dados fornecidos. Erro: {e}"
        )

def listar_vagas_abertas():
    return vaga_repository.find_all_vagas()

def buscar_vaga_por_id(vaga_id: int):
    vaga = vaga_repository.find_vaga_by_id(vaga_id)
    if not vaga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaga não encontrada.")
    return vaga

def atualizar_vaga(vaga_id: int, vaga_data: dict):
    vaga_existente = buscar_vaga_por_id(vaga_id)
    success = vaga_repository.update_existing_vaga(vaga_id, vaga_data)
    if success: 
        return vaga_repository.find_vaga_by_id(vaga_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível atualizar a vaga.")

def finalizar_vaga(vaga_id: int):
    vaga_existente = buscar_vaga_por_id(vaga_id)
    success = vaga_repository.finalize_vaga_by_id(vaga_id)
    if success: 
        return vaga_repository.find_vaga_by_id(vaga_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível finalizar a vaga.")