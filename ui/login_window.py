from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from ui.main_window import MainWindow
from auth import authenticate

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Mercadinho")
        self.resize(300, 200)

        layout = QVBoxLayout()
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Senha")
        self.password.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton("Entrar")
        self.login_btn.clicked.connect(self.login)

        layout.addWidget(QLabel("Acesso ao sistema"))
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def login(self):
        email = self.email.text().strip()
        password = self.password.text().strip()
        user = authenticate(email, password)
        if user:
            QMessageBox.information(self, "Sucesso", f"Bem-vindo, {user['name']}!")
            self.hide()
            self.main = MainWindow(user)
            self.main.show()
        else:
            QMessageBox.warning(self, "Erro", "Email ou senha inválidos.")
