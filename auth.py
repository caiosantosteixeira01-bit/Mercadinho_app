from models import get_connection, hash_password

def authenticate(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, phone, password, user_type_id
        FROM users
        WHERE email = ?
    """, (email,))
    
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    user_id, name, email, phone, stored_password, user_type_id = row

    # Validação da senha
    if stored_password != hash_password(password):
        return None

    # Retorna um dicionário consistente
    return {
        "id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "password": stored_password,
        "user_type_id": user_type_id   # importante!
    }
