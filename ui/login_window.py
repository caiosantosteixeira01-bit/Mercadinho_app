from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from ui.main_window import MainWindow
from auth import authenticate
from db import get_connection

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Mercadinho")
        self.resize(500, 500)

        # ----------------------
        # Ícone da janela
        # ----------------------
        self.setWindowIcon(QIcon("assets/logo.png"))  # caminho da imagem do ícone (.ico ou .png)

        layout = QVBoxLayout()

        # ----------------------
        # Logo
        # ----------------------
        self.logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(500, 500)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Senha")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Entrar")
        self.login_btn.clicked.connect(self.login)

        layout.addWidget(self.logo_label)
        layout.addWidget(QLabel("Acesso ao sistema"))
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def login(self):
        user = authenticate(self.email.text(), self.password.text())
        if not user:
            QMessageBox.warning(self, "Erro", "Email ou senha incorretos.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM user_types WHERE id = ?", (user["user_type_id"],))
        tipo_nome = cur.fetchone()[0]
        conn.close()

        user_info = (
            user["id"],
            user["name"],
            user["email"],
            user["phone"],
            user["password"],
            tipo_nome
        )

        QMessageBox.information(self, "Sucesso", f"Bem-vindo, {user['name']}!")
        self.hide()
        self.main = MainWindow(user_info)
        self.main.show()
