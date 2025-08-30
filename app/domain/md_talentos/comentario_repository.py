import pandas as pd
import json
from app.infra.database import get_db_connection
from psycopg2.extras import DictCursor

def find_talentos_by_vaga_id(vaga_id: int) -> pd.DataFrame:
    with get_db_connection() as conn:
        sql_query = "SELECT * FROM talentos WHERE vaga_id = %s;"
        df = pd.read_sql_query(sql_query, conn, params=(vaga_id,))
        return df

def create_new_talento(talento_data: dict, embedding: list):
    sql = """
        INSERT INTO talentos (
            vaga_id, nome, email, cidade, telefone, sobre_mim, experiencia_profissional, 
            formacao, idiomas, respostas_criterios, respostas_diferenciais, 
            redes_sociais, cursos_extracurriculares, deficiencia, deficiencia_detalhes, 
            aceita_termos, confirmar_dados_verdadeiros, embedding, ativo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                talento_data['vaga_id'], talento_data['nome'], talento_data['email'],
                talento_data.get('cidade'), talento_data.get('telefone'), talento_data['sobre_mim'],
                json.dumps(talento_data.get('experiencia_profissional')),
                json.dumps(talento_data.get('formacao')),
                json.dumps(talento_data.get('idiomas')),
                json.dumps(talento_data.get('respostas_criterios')),
                json.dumps(talento_data.get('respostas_diferenciais')),
                json.dumps(talento_data.get('redes_sociais')),
                json.dumps(talento_data.get('cursos_extracurriculares')),
                talento_data.get('deficiencia', False),
                json.dumps(talento_data.get('deficiencia_detalhes')),
                talento_data['aceita_termos'],
                talento_data['confirmar_dados_verdadeiros'],
                str(embedding),
                talento_data.get('ativo', True)
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id

def _parse_json_fields(records: list) -> list:
    json_fields = [
        'experiencia_profissional', 'formacao', 'idiomas', 
        'respostas_criterios', 'respostas_diferenciais', 'redes_sociais', 
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
    sql = """
        SELECT t.*, v.area_id, a.nome AS nome_area
        FROM talentos t
        LEFT JOIN vagas v ON t.vaga_id = v.id
        LEFT JOIN areas a ON v.area_id = a.id
        ORDER BY t.criado_em DESC;
    """
    with get_db_connection() as conn:
        df = pd.read_sql_query(sql, conn)
        records = df.to_dict(orient='records')
        # Adicionar aqui a busca de comentários para cada talento se necessário na listagem geral
        return _parse_json_fields(records)

def find_talento_by_id(talento_id: int):
    sql_query = """
        SELECT t.*, v.area_id, a.nome AS nome_area
        FROM talentos t
        LEFT JOIN vagas v ON t.vaga_id = v.id
        LEFT JOIN areas a ON v.area_id = a.id
        WHERE t.id = %s;
    """
    with get_db_connection() as conn:
        df = pd.read_sql_query(sql_query, conn, params=(talento_id,))
        if not df.empty:
            record = df.iloc[0].to_dict()
            parsed_record = _parse_json_fields([record])[0]
            parsed_record['comentarios'] = find_comments_by_talento_id(talento_id)
            return parsed_record
    return None

# --- NOVAS FUNÇÕES PARA COMENTÁRIOS ---

def create_comment(texto: str, talento_id: int, user_id: int):
    sql = """
        INSERT INTO comentarios_talentos (texto, talento_id, user_id)
        VALUES (%s, %s, %s) RETURNING id;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (texto, talento_id, user_id))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id

def find_comment_by_id(comment_id: int):
    sql = "SELECT * FROM comentarios_talentos WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (comment_id,))
            comment = cur.fetchone()
            return dict(comment) if comment else None

def find_comments_by_talento_id(talento_id: int):
    sql = """
        SELECT c.*, u.nome as user_nome
        FROM comentarios_talentos c
        JOIN users u ON c.user_id = u.id
        WHERE c.talento_id = %s
        ORDER BY c.criado_em ASC;
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (talento_id,))
            comments = cur.fetchall()
            return [dict(row) for row in comments]

def delete_comment_by_id(comment_id: int):
    sql = "DELETE FROM comentarios_talentos WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (comment_id,))
            conn.commit()
            return cur.rowcount > 0