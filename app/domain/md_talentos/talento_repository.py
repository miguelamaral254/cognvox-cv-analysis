import pandas as pd
import json
from app.infra.database import get_db_connection

def find_talentos_by_vaga_id(vaga_id: int) -> pd.DataFrame:
    with get_db_connection() as conn:
        sql_query = "SELECT * FROM talentos WHERE vaga_id = %s;"
        df = pd.read_sql_query(sql_query, conn, params=(vaga_id,))
        return df

def create_new_talento(talento_data: dict, embedding: list):
    sql = """
        INSERT INTO talentos (vaga_id, nome, email, sobre_mim, experiencia_profissional, formacao, aceita_termos, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                talento_data['vaga_id'], talento_data['nome'], talento_data['email'],
                talento_data['sobre_mim'], json.dumps(talento_data.get('experiencia_profissional')),
                talento_data['formacao'], talento_data['aceita_termos'], str(embedding)
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id

def find_all_talentos():
    with get_db_connection() as conn:
        sql = "SELECT * FROM talentos ORDER BY criado_em DESC;"
        df = pd.read_sql_query(sql, conn)
        
        records = df.to_dict(orient='records')
        
        for record in records:
            exp = record.get('experiencia_profissional')
            
            if exp and isinstance(exp, dict):
                record['experiencia_profissional'] = [exp]
        
        return records

def find_talento_by_id(talento_id: int):
    with get_db_connection() as conn:
        sql_query = "SELECT * FROM talentos WHERE id = %s;"
        df = pd.read_sql_query(sql_query, conn, params=(talento_id,))

        if not df.empty:
            return df.iloc[0].to_dict()
    return None