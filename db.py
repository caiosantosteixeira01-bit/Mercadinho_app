import sqlite3
import os

DB_NAME = "data/database.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela tipos de usuário
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    # Tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT,
        user_type_id INTEGER,
        is_on INTEGER DEFAULT 0,
        FOREIGN KEY(user_type_id) REFERENCES user_types(id)
    )
    """)

    # Tabela de produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER,
        price REAL
    )
    """)

    # Inserir tipos de usuário padrão
    cursor.execute("INSERT OR IGNORE INTO user_types (id, name) VALUES (1,'Admin'),(2,'Moderador'),(3,'Limitado')")
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
