import pandas as pd
import json
from app.infra.database import get_db_connection

def _parse_vaga_json_fields(vaga_dict):
    """Função auxiliar para converter campos JSON de string para dict."""
    if not vaga_dict:
        return vaga_dict
    
    json_fields = ['criterios_de_analise', 'criterios_diferenciais_de_analise']
    for field in json_fields:
        if vaga_dict.get(field) and isinstance(vaga_dict[field], str):
            try:
                vaga_dict[field] = json.loads(vaga_dict[field])
            except json.JSONDecodeError:
                # Mantém o valor original se não for um JSON válido
                pass
    return vaga_dict

def find_vaga_by_id(vaga_id: int):
    sql = """
        SELECT 
            vagas.*, 
            areas.nome AS nome_area
        FROM 
            vagas
        LEFT JOIN 
            areas ON vagas.area_id = areas.id
        WHERE 
            vagas.id = %s;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (vaga_id,))
            vaga = cur.fetchone()
            if vaga:
                columns = [desc[0] for desc in cur.description]
                vaga_dict = dict(zip(columns, vaga))
                # Converte os campos JSON antes de retornar
                return _parse_vaga_json_fields(vaga_dict)
    return None

def find_all_vagas():
    sql = """
        SELECT 
            vagas.*, 
            areas.nome AS nome_area
        FROM 
            vagas
        LEFT JOIN 
            areas ON vagas.area_id = areas.id;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            vagas = cur.fetchall()
            if not vagas:
                return []
            columns = [desc[0] for desc in cur.description]
            vagas_list = [dict(zip(columns, row)) for row in vagas]
            return [_parse_vaga_json_fields(vaga) for vaga in vagas_list]
def create_new_vaga(vaga_data: dict, criado_por: int):
    sql = """
        INSERT INTO vagas (
            titulo_vaga, descricao, cidade, modelo_trabalho, area_id, 
            criterios_de_analise, vaga_pcd, criterios_diferenciais_de_analise,
            criado_por
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                vaga_data['titulo_vaga'],
                vaga_data['descricao'],
                vaga_data['cidade'],
                vaga_data['modelo_trabalho'],
                vaga_data['area_id'],
                json.dumps(vaga_data['criterios_de_analise']),
                vaga_data.get('vaga_pcd', False),
                json.dumps(vaga_data.get('criterios_diferenciais_de_analise')),
                criado_por
            ))
            new_id = cur.lastrowid
            conn.commit()
            return new_id

def update_existing_vaga(vaga_id: int, vaga_data: dict):
    sql = """
        UPDATE vagas SET 
            titulo_vaga = %s, 
            descricao = %s, 
            cidade = %s, 
            modelo_trabalho = %s, 
            area_id = %s, 
            criterios_de_analise = %s,
            vaga_pcd = %s,
            criterios_diferenciais_de_analise = %s
        WHERE id = %s;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                vaga_data['titulo_vaga'],
                vaga_data['descricao'],
                vaga_data['cidade'],
                vaga_data['modelo_trabalho'],
                vaga_data['area_id'],
                json.dumps(vaga_data['criterios_de_analise']),
                vaga_data.get('vaga_pcd', False),
                json.dumps(vaga_data.get('criterios_diferenciais_de_analise')),
                vaga_id
            ))
            conn.commit()
            return cur.rowcount > 0

def finalize_vaga_by_id(vaga_id: int, finalizado_por: int):
    sql = "UPDATE vagas SET finalizada_em = CURRENT_TIMESTAMP, finalizado_por = %s WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (finalizado_por, vaga_id))
            conn.commit()
            return cur.rowcount > 0

def save_ranking(vaga_id: int, ranking_data: list):
    delete_sql = "DELETE FROM top_aplicantes WHERE vaga_id = %s;"
    insert_sql = "INSERT INTO top_aplicantes (vaga_id, talento_id, score_final, scores_por_criterio) VALUES (%s, %s, %s, %s);"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(delete_sql, (vaga_id,))
            for rank in ranking_data:
                params = (vaga_id, rank['id'], rank['score_final'], json.dumps(rank['scores_detalhados']))
                cur.execute(insert_sql, params)
        conn.commit()