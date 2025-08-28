import os
from dotenv import load_dotenv
from .database import get_db_connection

def run_migrations():
    load_dotenv()

    if os.getenv('ISDEV') != 'true':
        print("⚪ Modo de produção detectado. Pulando migrações automáticas.")
        return

    print("🔎 Verificando e executando migrações do banco de dados (Modo DEV)...")
    
    migrations_path = "db/migrations"
    
    if not os.path.exists(migrations_path):
        print(f"⚠️  Pasta de migrações '{migrations_path}' não encontrada. Pulando.")
        return

    migration_files = sorted([f for f in os.listdir(migrations_path) if f.endswith('.sql')])

    if not migration_files:
        print("✅ Nenhuma migração para executar.")
        return

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                for filename in migration_files:
                    print(f"  - Executando migração: {filename} ...")
                    filepath = os.path.join(migrations_path, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        sql_script = file.read()
                        cur.execute(sql_script)
                conn.commit()
        print("✅ Migrações do banco de dados executadas com sucesso!")
    except Exception as e:
        print(f"🚨 Erro ao executar migrações: {e}")
        raise