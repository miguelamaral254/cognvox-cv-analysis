from app.infra.database import get_db_connection

def create_comment(texto: str, talento_id: int, user_id: int):
    sql = """
        INSERT INTO comentarios_talentos (texto, talento_id, user_id)
        VALUES (%s, %s, %s);
    """ 
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (texto, talento_id, user_id))
            new_id = cur.lastrowid  
            conn.commit()
            return new_id

def find_comment_by_id(comment_id: int):
    sql = "SELECT * FROM comentarios_talentos WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (comment_id,))
            comment = cur.fetchone()
            return comment if comment else None

def find_comments_by_talento_id(talento_id: int):
    sql = """
        SELECT c.*, u.nome as user_nome
        FROM comentarios_talentos c
        JOIN users u ON c.user_id = u.id
        WHERE c.talento_id = %s;
    """
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (talento_id,))
            comments = cur.fetchall()
            return comments

def delete_comment_by_id(comment_id: int):
    sql = "DELETE FROM comentarios_talentos WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (comment_id,))
            conn.commit()
            return cur.rowcount > 0
def find_comments_by_talento_ids(talento_ids: list[int]):
    if not talento_ids:
        return []

    placeholders = ', '.join(['%s'] * len(talento_ids))
    
    sql = f"""
        SELECT c.*, u.nome as user_nome
        FROM comentarios_talentos c
        JOIN users u ON c.user_id = u.id
        WHERE c.talento_id IN ({placeholders});
    """
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, tuple(talento_ids))
            comments = cur.fetchall()
            return comments