from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from db import init_db
import sys

if __name__ == "__main__":
    init_db()  # Cria banco e tabelas
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
