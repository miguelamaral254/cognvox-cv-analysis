import pandas as pd
import json
from app.infra.database import get_db_connection

def find_vaga_by_id(vaga_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, titulo_vaga, criterios_de_analise, top_x_candidatos, criado_em, finalizada_em FROM vagas WHERE id = %s",
                (vaga_id,)
            )
            vaga = cur.fetchone()
            if vaga:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, vaga))
    return None

def find_all_vagas():
    with get_db_connection() as conn:
        sql = "SELECT * FROM vagas WHERE finalizada_em IS NULL ORDER BY criado_em DESC;"
        df = pd.read_sql_query(sql, conn)
        return df.to_dict(orient='records')

def create_new_vaga(vaga_data: dict):
    sql = "INSERT INTO vagas (titulo_vaga, criterios_de_analise, top_x_candidatos) VALUES (%s, %s, %s) RETURNING id;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                vaga_data['titulo_vaga'], 
                json.dumps(vaga_data['criterios_de_analise']), 
                vaga_data['top_x_candidatos']
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id

def update_existing_vaga(vaga_id: int, vaga_data: dict):
    sql = "UPDATE vagas SET titulo_vaga = %s, criterios_de_analise = %s, top_x_candidatos = %s WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                vaga_data['titulo_vaga'], json.dumps(vaga_data['criterios_de_analise']), 
                vaga_data['top_x_candidatos'], vaga_id
            ))
            conn.commit()
            return cur.rowcount > 0

def finalize_vaga_by_id(vaga_id: int):
    sql = "UPDATE vagas SET finalizada_em = CURRENT_TIMESTAMP WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (vaga_id,))
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