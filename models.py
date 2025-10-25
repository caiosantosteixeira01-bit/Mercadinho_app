from db import get_connection

class User:
    def __init__(self, id, name, email, phone, password, user_type_id, is_on):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.user_type_id = user_type_id
        self.is_on = is_on

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.phone, u.password, ut.type_name, u.is_on
            FROM users u
            JOIN user_types ut ON u.user_type_id = ut.id
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def create(name, email, phone, password, user_type_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, phone, password, user_type_id)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, password, user_type_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update(user_id, name, email, phone, password, user_type_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET name=?, email=?, phone=?, password=?, user_type_id=?
            WHERE id=?
        """, (name, email, phone, password, user_type_id, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

class Product:
    def __init__(self, id, name, category, quantity, price_purchase, price_sale):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price_purchase = price_purchase
        self.price_sale = price_sale

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def create(name, category, quantity, price_purchase, price_sale):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, category, quantity, price_purchase, price_sale)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, quantity, price_purchase, price_sale))
        conn.commit()
        conn.close()

    @staticmethod
    def update(product_id, name, category, quantity, price_purchase, price_sale):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name=?, category=?, quantity=?, price_purchase=?, price_sale=?
            WHERE id=?
        """, (name, category, quantity, price_purchase, price_sale, product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
