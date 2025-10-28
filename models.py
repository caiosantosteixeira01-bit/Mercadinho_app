import sqlite3
from db import get_connection
import bcrypt

class User:
    @staticmethod
    def create(name, email, phone, password, user_type_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user_types WHERE name=?", (user_type_name,))
        user_type_id = cursor.fetchone()[0]

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor.execute("""
        INSERT INTO users (name,email,phone,password,user_type_id)
        VALUES (?,?,?,?,?)
        """, (name,email,phone,hashed,user_type_id))
        conn.commit()
        conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.name, u.email, u.phone, ut.name, u.is_on
        FROM users u
        JOIN user_types ut ON u.user_type_id = ut.id
    """)
    users = cursor.fetchall()
    conn.close()
    return users

def update_user(user_id, name, email, phone, password, user_type_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_types WHERE name=?", (user_type_name,))
    user_type_id = cursor.fetchone()[0]

    if password:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("""
            UPDATE users SET name=?, email=?, phone=?, password=?, user_type_id=? WHERE id=?
        """, (name,email,phone,hashed,user_type_id,user_id))
    else:
        cursor.execute("""
            UPDATE users SET name=?, email=?, phone=?, user_type_id=? WHERE id=?
        """, (name,email,phone,user_type_id,user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

# Produtos
class Product:
    @staticmethod
    def create(name, quantity, price):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name,quantity,price) VALUES (?,?,?)", (name,quantity,price))
        conn.commit()
        conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def update_product(product_id, name, quantity, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=?,quantity=?,price=? WHERE id=?", (name,quantity,price,product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
