from PyQt6.QtWidgets import QDialog,QVBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox
from ui.main_window import MainWindow
from auth import login

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Mercadinho App")
        self.resize(400,200)

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Entrar")
        self.btn_login.clicked.connect(self.try_login)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Senha:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def try_login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if login(email,password):
            self.accept()
            self.main = MainWindow()
            self.main.show()
        else:
            QMessageBox.warning(self,"Erro","Email ou senha incorretos")
