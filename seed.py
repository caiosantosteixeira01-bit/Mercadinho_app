from db import get_connection, init_db
from models import hash_password


def seed_data():
    # Recria as tabelas
    init_db()

    conn = get_connection()
    cur = conn.cursor()

    print("🔧 Criando tipos de usuário...")

    # Tipos de usuário
    user_types = ["ADMIN", "MOD", "LIMITADO"]
    for t in user_types:
        cur.execute("INSERT OR IGNORE INTO user_types (name) VALUES (?)", (t,))

    print("👤 Criando usuários padrão...")

    # Usuário ADMIN
    cur.execute("""
        INSERT OR IGNORE INTO users (name, email, phone, password, user_type_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Administrador",
        "admin@admin.com",
        "41999999999",
        hash_password("admin123"),
        1  # ADMIN
    ))

    # Usuário MODERADOR
    cur.execute("""
        INSERT OR IGNORE INTO users (name, email, phone, password, user_type_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Moderador",
        "mod@admin.com",
        "41988888888",
        hash_password("mod123"),
        2  # MOD
    ))

    # Usuário LIMITADO
    cur.execute("""
        INSERT OR IGNORE INTO users (name, email, phone, password, user_type_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Usuário Limitado",
        "user@admin.com",
        "41977777777",
        hash_password("user123"),
        3  # LIMITADO
    ))

    print("📦 Inserindo produtos de exemplo...")

    sample_products = [
        ("Arroz 5kg", 22.50, 30),
        ("Feijão 1kg", 8.90, 50),
        ("Óleo 900ml", 6.50, 40),
        ("Macarrão 500g", 4.80, 100),
        ("Açúcar 1kg", 3.90, 80),
    ]

    for name, price, stock in sample_products:
        cur.execute("""
            INSERT OR IGNORE INTO products (name, price, stock)
            VALUES (?, ?, ?)
        """, (name, price, stock))

    conn.commit()
    conn.close()
    print("✅ Banco criado e preenchido com sucesso!")


if __name__ == "__main__":
    seed_data()
