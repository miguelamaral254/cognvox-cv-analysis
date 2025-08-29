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
        INSERT INTO talentos (
            vaga_id, nome, email, cidade, telefone, sobre_mim, 
            experiencia_profissional, formacao, idiomas, respostas_criterios, 
            respostas_diferenciais, redes_sociais, cursos_extracurriculares, 
            deficiencia, deficiencia_detalhes, aceita_termos, 
            confirmar_dados_verdadeiros, embedding
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                talento_data['vaga_id'],
                talento_data['nome'],
                talento_data['email'],
                talento_data.get('cidade'),
                talento_data.get('telefone'),
                talento_data['sobre_mim'],
                json.dumps(talento_data.get('experiencia_profissional')),
                json.dumps(talento_data.get('formacao')),
                json.dumps(talento_data.get('idiomas')),
                json.dumps(talento_data.get('respostas_criterios')),
                json.dumps(talento_data.get('respostas_diferenciais')), # <-- CAMPO ADICIONADO
                json.dumps(talento_data.get('redes_sociais')),
                json.dumps(talento_data.get('cursos_extracurriculares')),
                talento_data.get('deficiencia', False),
                json.dumps(talento_data.get('deficiencia_detalhes')),
                talento_data['aceita_termos'],
                talento_data['confirmar_dados_verdadeiros'],
                str(embedding)
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id

def _parse_json_fields(records: list) -> list:
    json_fields = [
        'experiencia_profissional', 'formacao', 'idiomas', 
        'respostas_criterios', 'respostas_diferenciais', 'redes_sociais', # <-- CAMPO ADICIONADO
        'cursos_extracurriculares', 'deficiencia_detalhes'
    ]
    for record in records:
        for field in json_fields:
            if isinstance(record.get(field), str):
                try:
                    record[field] = json.loads(record[field])
                except json.JSONDecodeError:
                    pass
    return records

def find_all_talentos():
    with get_db_connection() as conn:
        sql = "SELECT * FROM talentos ORDER BY criado_em DESC;"
        df = pd.read_sql_query(sql, conn)
        records = df.to_dict(orient='records')
        return _parse_json_fields(records)

def find_talento_by_id(talento_id: int):
    with get_db_connection() as conn:
        sql_query = "SELECT * FROM talentos WHERE id = %s;"
        df = pd.read_sql_query(sql_query, conn, params=(talento_id,))
        if not df.empty:
            record = df.iloc[0].to_dict()
            return _parse_json_fields([record])[0]
    return None

def find_and_format_talentos_by_vaga_id(vaga_id: int) -> list:
    with get_db_connection() as conn:
        sql_query = "SELECT * FROM talentos WHERE vaga_id = %s ORDER BY criado_em DESC;"
        df = pd.read_sql_query(sql_query, conn, params=(vaga_id,))
        if df.empty:
            return []
        records = df.to_dict(orient='records')
        return _parse_json_fields(records)
