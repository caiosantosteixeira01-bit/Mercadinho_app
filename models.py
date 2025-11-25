import sqlite3
import hashlib

DB_NAME = "mercadinho.db"

# ==========================================================
# 🔗 Conexão com banco
# ==========================================================
def get_connection():
    return sqlite3.connect(DB_NAME)

# ==========================================================
# 🔒 Criptografia de senha
# ==========================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ==========================================================
# 👥 CRUD Usuários
# ==========================================================
class User:
    @staticmethod
    def create(name, email, phone, password, user_type_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users (name, email, phone, password, user_type_id)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, phone, hash_password(password), user_type_id))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Erro: email já existe.")
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(user_id, name, email, phone, user_type_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE users SET name=?, email=?, phone=?, user_type_id=?
            WHERE id=?
        """, (name, email, phone, user_type_id, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_email(email):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT users.id, users.name, users.email, users.phone, users.password, user_types.name
            FROM users
            JOIN user_types ON users.user_type_id = user_types.id
            WHERE users.email = ?
        """, (email,))
        user = cur.fetchone()
        conn.close()
        return user

# ==========================================================
# 📦 CRUD Produtos
# ==========================================================
class Product:
    @staticmethod
    def create(name, price, stock):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO products (name, price, stock)
            VALUES (?, ?, ?)
        """, (name, price, stock))
        conn.commit()
        conn.close()

    @staticmethod
    def update(product_id, name, price, stock):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE products SET name=?, price=?, stock=?
            WHERE id=?
        """, (name, price, stock, product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()

# ==========================================================
# 📋 Funções auxiliares
# ==========================================================
def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT users.id, users.name, users.email, users.phone, user_types.name
        FROM users
        JOIN user_types ON users.user_type_id = user_types.id
    """)
    users = cur.fetchall()
    conn.close()
    return users

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT users.id, users.name, users.email, users.phone, users.password, user_types.name
        FROM users
        JOIN user_types ON users.user_type_id = user_types.id
        WHERE users.email = ?
    """, (email,))
    user = cur.fetchone()
    conn.close()
    return user

def get_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price, stock FROM products")
    products = cur.fetchall()
    conn.close()
    return products

# ==========================================================
# 🧱 Criação das tabelas (caso não existam)
# ==========================================================
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Tipos de usuários
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Usuários
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            user_type_id INTEGER NOT NULL,
            FOREIGN KEY (user_type_id) REFERENCES user_types (id)
        )
    """)

    # Produtos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Cria tipos padrão (se não existirem)
    cur.execute("INSERT OR IGNORE INTO user_types (id, name) VALUES (1, 'ADMIN')")
    cur.execute("INSERT OR IGNORE INTO user_types (id, name) VALUES (2, 'MOD')")
    cur.execute("INSERT OR IGNORE INTO user_types (id, name) VALUES (3, 'LIMITADO')")

    conn.commit()
    conn.close()
