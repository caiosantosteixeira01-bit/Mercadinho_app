from db import get_connection

def login(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.name, u.email, ut.type_name
        FROM users u
        JOIN user_types ut ON u.user_type_id = ut.id
        WHERE email=? AND password=?
    """, (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def can_create(logged_type, new_type):
    if logged_type == "ADMIN":
        return True
    elif logged_type == "MOD" and new_type == "LIMITADO":
        return True
    return False


