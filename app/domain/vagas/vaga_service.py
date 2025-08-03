# app/domain/vagas/vaga_service.py
from app.infra import repositories
from app.domain.analysis import analysis_service

def formatar_experiencia(exp_json):
    if not exp_json or not isinstance(exp_json, list): return ""
    textos = [f"Cargo: {exp.get('cargo', '')}. Descrição: {exp.get('descricao', '')}" for exp in exp_json]
    return " ".join(textos)

# --- Serviço de Análise ---
def analisar_e_ranquear_vaga(vaga_id: int):
    params_vaga = repositories.find_vaga_by_id(vaga_id)
    if not params_vaga or params_vaga.get("finalizada_em"): return None
    
    df_candidatos = repositories.find_talentos_by_vaga_id(vaga_id)
    if df_candidatos.empty: return {"titulo_vaga": params_vaga["titulo_vaga"], "ranking": []}

    if 'experiencia_profissional' in df_candidatos.columns:
        df_candidatos['experiencia_formatada'] = df_candidatos['experiencia_profissional'].apply(formatar_experiencia)

    criterios = params_vaga["criterios_de_analise"]
    df_analisado = analysis_service.calcular_similaridade(df_candidatos, criterios)

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

    repositories.save_ranking(vaga_id, ranking_para_salvar)
    return {"titulo_vaga": params_vaga["titulo_vaga"], "ranking": ranking_para_resposta}

# --- Serviços de CRUD ---
def criar_nova_vaga(vaga_data: dict):
    vaga_id = repositories.create_new_vaga(vaga_data)
    return repositories.find_vaga_by_id(vaga_id)

def listar_vagas_abertas():
    return repositories.find_all_vagas()

def buscar_vaga_por_id(vaga_id: int):
    return repositories.find_vaga_by_id(vaga_id)

def atualizar_vaga(vaga_id: int, vaga_data: dict):
    success = repositories.update_existing_vaga(vaga_id, vaga_data)
    if success: return repositories.find_vaga_by_id(vaga_id)
    return None

def finalizar_vaga(vaga_id: int):
    success = repositories.finalize_vaga_by_id(vaga_id)
    if success: return repositories.find_vaga_by_id(vaga_id)
    return None