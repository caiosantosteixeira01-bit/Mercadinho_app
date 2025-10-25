import sqlite3

DB_NAME = "mercadinho.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de tipos de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT UNIQUE
        )
    """)

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            password TEXT NOT NULL,
            user_type_id INTEGER NOT NULL,
            is_on INTEGER DEFAULT 0,
            FOREIGN KEY(user_type_id) REFERENCES user_types(id)
        )
    """)

    # Tipos padrão
    cursor.execute("INSERT OR IGNORE INTO user_types (id, type_name) VALUES (1, 'ADMIN')")
    cursor.execute("INSERT OR IGNORE INTO user_types (id, type_name) VALUES (2, 'MOD')")
    cursor.execute("INSERT OR IGNORE INTO user_types (id, type_name) VALUES (3, 'LIMITADO')")

    # Tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            price_purchase REAL DEFAULT 0.0,
            price_sale REAL DEFAULT 0.0
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
