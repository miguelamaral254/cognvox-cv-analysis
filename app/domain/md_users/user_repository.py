from app.infra.database import get_db_connection
from .user_schema import UserCreate, UserProfileUpdate, RoleCreate, RoleUpdate
from app.domain.md_auth.password_utils import get_password_hash

def get_user_by_email(email: str):
    # SQL CORRIGIDO: Usa LEFT JOIN para garantir que o usuário seja sempre retornado
    sql = """
        SELECT
            u.*,
            ur.nome AS role
        FROM
            users u
        LEFT JOIN
            user_role ur ON u.user_role_id = ur.id
        WHERE
            TRIM(u.email) = %s;
    """
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return user if user else None
def find_user_by_id(user_id: int):
    sql = """
        SELECT
            u.*,
            ur.nome AS role
        FROM
            users u
        LEFT JOIN
            user_role ur ON u.user_role_id = ur.id
        WHERE
            u.id = %s;
    """
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (user_id,))
            user = cur.fetchone()
            return user if user else None

def find_all_users():
    sql = """
        SELECT
            u.*,
            ur.nome AS role
        FROM
            users u
        LEFT JOIN
            user_role ur ON u.user_role_id = ur.id
        ORDER BY
            u.nome ASC;
    """
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql)
            users = cur.fetchall()
            return users

def create_user(user_data: UserCreate):
    sql = """
        INSERT INTO users (nome, email, hashed_password, user_role_id)
        VALUES (%s, %s, %s, %s);
    """
    hashed_password = get_password_hash(user_data.password)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                user_data.nome,
                user_data.email,
                hashed_password,
                user_data.user_role_id,
            ))
            conn.commit()
    return get_user_by_email(user_data.email)

def update_profile(user_id: int, profile_data: UserProfileUpdate):
    sql = "UPDATE users SET nome = %s, email = %s WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (profile_data.nome, profile_data.email, user_id))
            conn.commit()
            return cur.rowcount > 0

def update_password(user_id: int, new_hashed_password: str):
    sql = "UPDATE users SET hashed_password = %s WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (new_hashed_password, user_id))
            conn.commit()
            return cur.rowcount > 0

def set_user_active_status(user_id: int, is_active: bool):
    sql = "UPDATE users SET is_active = %s WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (is_active, user_id))
            conn.commit()
            return cur.rowcount > 0
def find_role_by_id(role_id: int):
    sql = "SELECT * FROM user_role WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (role_id,))
            return cur.fetchone()

def find_role_by_name(nome: str):
    sql = "SELECT * FROM user_role WHERE nome = %s;"
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (nome,))
            return cur.fetchone()

def find_all_roles():
    sql = "SELECT * FROM user_role ORDER BY nome ASC;"
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql)
            return cur.fetchall()

def create_role(role_data: RoleCreate):
    sql = "INSERT INTO user_role (nome) VALUES (%s);"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (role_data.nome,))
            new_id = cur.lastrowid
            conn.commit()
            return find_role_by_id(new_id)

def update_role(role_id: int, role_data: RoleUpdate):
    sql = "UPDATE user_role SET nome = %s WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (role_data.nome, role_id))
            conn.commit()
            return cur.rowcount > 0

def delete_role(role_id: int):
    sql = "DELETE FROM user_role WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (role_id,))
            conn.commit()
            return cur.rowcount > 0

def count_users_by_role_id(role_id: int):
    sql = "SELECT COUNT(*) as total FROM users WHERE user_role_id = %s;"
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (role_id,))
            result = cur.fetchone()
            return result['total'] if result else 0