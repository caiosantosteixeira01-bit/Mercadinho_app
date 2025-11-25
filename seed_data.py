from models import User, hash_password, get_connection, create_tables

def seed():
    # Garante que as tabelas existam
    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se já há usuários no banco
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        users = [
            ("Administrador", "admin@mercado.com", "9999-0000", hash_password("admin123"), 1),
            ("Moderador", "mod@mercado.com", "9999-0001", hash_password("mod123"), 2),
            ("Limitado", "limitado@mercado.com", "9999-0002", hash_password("lim123"), 3)
        ]

        cursor.executemany(
            "INSERT INTO users (name, email, phone, password, user_type_id) VALUES (?, ?, ?, ?, ?)",
            users
        )
        conn.commit()
        print("✅ Usuários de teste criados com sucesso!")
    else:
        print("ℹ️ Usuários já existentes no banco.")

    conn.close()


if __name__ == "__main__":
    seed()
