from app.infra.database import get_db_connection

def _map_row_to_dict(row, cursor):
    if not row:
        return None
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))

# app/domain/md_vagas/area_repository.py

def create_area(area_data: dict):
    # 1. Removido o "RETURNING id" da query SQL
    sql = "INSERT INTO areas (nome, descricao) VALUES (%s, %s);"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (area_data['nome'], area_data.get('descricao')))
            # 2. Usamos 'cur.lastrowid' para obter o ID do item inserido no MySQL
            new_id = cur.lastrowid
            conn.commit()
            return new_id
def find_area_by_id(area_id: int):
    """Busca uma área pelo seu ID."""
    sql = "SELECT * FROM areas WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (area_id,))
            area = cur.fetchone()
            return _map_row_to_dict(area, cur)

# app/domain/md_vagas/area_repository.py

def find_area_by_name(nome: str):
    sql = "SELECT * FROM areas WHERE nome = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nome,))
            area = cur.fetchone()
            return _map_row_to_dict(area, cur)
def find_all_areas():
    """Busca todas as áreas cadastradas."""
    sql = "SELECT * FROM areas ORDER BY nome;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            areas = cur.fetchall()
            if not areas:
                return []
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in areas]

def update_area(area_id: int, area_data: dict):
    fields = []
    params = []
    for key, value in area_data.items():
        if value is not None:
            fields.append(f"{key} = %s")
            params.append(value)

    if not fields:
        return True 

    params.append(area_id)
    sql = f"UPDATE areas SET {', '.join(fields)} WHERE id = %s;"

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            conn.commit()
            return cur.rowcount > 0

def delete_area(area_id: int):
    sql = "DELETE FROM areas WHERE id = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (area_id,))
            conn.commit()
            return cur.rowcount > 0