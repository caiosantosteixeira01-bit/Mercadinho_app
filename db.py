import sqlite3

DB_NAME = "mercadinho.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # ============================
    # TABELA DOS TIPOS DE USUÁRIO
    # ============================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # ============================
    # TABELA DE USUÁRIOS
    # ============================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            user_type_id INTEGER NOT NULL,
            FOREIGN KEY (user_type_id) REFERENCES user_types(id)
        )
    """)

    # ============================
    # TABELA DE PRODUTOS
    # ============================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)

    # ============================
    # INSERIR TIPOS DE USUÁRIOS
    # ============================
    cur.execute("INSERT OR IGNORE INTO user_types (id, name) VALUES (1, 'ADMIN')")
    cur.execute("INSERT OR IGNORE INTO user_types (id, name) VALUES (2, 'MOD')")
    cur.execute("INSERT OR IGNORE INTO user_types (id, name) VALUES (3, 'LIMITADO')")

    conn.commit()
    conn.close()
