import os
import mysql.connector 
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"), 
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": os.getenv("DB_PORT")
}

@contextmanager
def get_db_connection():

    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except mysql.connector.Error as e:
        print(f"🚨 Erro de conexão com o banco de dados MySQL: {e}")
        raise
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
