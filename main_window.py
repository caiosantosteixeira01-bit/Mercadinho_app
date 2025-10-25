from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from ui.user_dialog import UserDialog
from ui.product_dialog import ProductDialog

class MainWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Mercadinho - Sistema")
        self.setFixedSize(400, 300)
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        welcome = QLabel(f"Bem-vindo, {self.user[1]} ({self.user[3]})")
        layout.addWidget(welcome)

        self.user_mgmt_btn = QPushButton("Gerenciar Usuários")
        self.user_mgmt_btn.clicked.connect(self.open_user_dialog)
        layout.addWidget(self.user_mgmt_btn)

        self.product_btn = QPushButton("Gerenciar Estoque")
        self.product_btn.clicked.connect(self.open_product_dialog)
        layout.addWidget(self.product_btn)

        self.setLayout(layout)

    def open_user_dialog(self):
        self.user_dialog = UserDialog(self.user)
        self.user_dialog.show()

    def open_product_dialog(self):
        self.product_dialog = ProductDialog(self.user)
        self.product_dialog.show()
