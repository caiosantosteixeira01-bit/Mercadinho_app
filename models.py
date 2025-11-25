from db import get_connection
import hashlib

# ==========================================================
# 🔐 Criptografia de senha
# ==========================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==========================================================
# 👥 USERS
# ==========================================================
def get_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.id, u.name, u.email, u.phone, ut.name
        FROM users u
        JOIN user_types ut ON ut.id = u.user_type_id
        ORDER BY u.id ASC
    """)

    users = cur.fetchall()
    conn.close()
    return users


class User:
    @staticmethod
    def create(name, email, phone, password, user_type_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (name, email, phone, password, user_type_id)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, hash_password(password), user_type_id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()


# ==========================================================
# 📦 PRODUCTS
# ==========================================================
def get_all_products():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, price, stock
        FROM products
        ORDER BY id ASC
    """)

    products = cur.fetchall()
    conn.close()
    return products


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
            UPDATE products
            SET name = ?, price = ?, stock = ?
            WHERE id = ?
        """, (name, price, stock, product_id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM products WHERE id = ?", (product_id,))

        conn.commit()
        conn.close()
