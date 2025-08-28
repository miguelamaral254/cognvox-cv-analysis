# app/domain/md_users/user_repository.py

from app.infra.database import get_db_connection
from .user_schema import UserCreate
from app.domain.md_auth.password_utils import get_password_hash # Importa do novo arquivo
from psycopg2.extras import DictCursor

def get_user_by_email(email: str):
    sql = "SELECT * FROM users WHERE email = %s;"
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return dict(user) if user else None

def find_user_by_id(user_id: int):
    # ... (código existente)
    sql = "SELECT * FROM users WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (user_id,))
            user = cur.fetchone()
            return dict(user) if user else None

def find_all_users():
    # ... (código existente)
    sql = "SELECT * FROM users ORDER BY nome ASC;"
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql)
            users = cur.fetchall()
            return [dict(row) for row in users]

def create_user(user_data: UserCreate):
    sql = """
        INSERT INTO users (nome, email, hashed_password, role, img_path)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    hashed_password = get_password_hash(user_data.password)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                user_data.nome,
                user_data.email,
                hashed_password,
                user_data.role.value,
                None 
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
    return get_user_by_email(user_data.email)