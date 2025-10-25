import sys
from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from create_db import create_tables
from seed_data import seed
from db import get_connection

def is_db_empty():
    """Verifica se a tabela de usuários está vazia"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

if __name__ == "__main__":
    create_tables()

    # Rodar seed somente se o banco estiver vazio
    if is_db_empty():
        seed()
        print("Seed inicial criado!")

    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
