from PyQt6.QtWidgets import QDialog,QVBoxLayout,QHBoxLayout,QPushButton,QLineEdit,QLabel,QTableWidget,QTableWidgetItem,QMessageBox
from models import Product,get_all_products,update_product,delete_product
from auth import current_user

class ProductDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Produtos")
        self.resize(600,400)

        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantidade")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Preço")

        form_layout.addWidget(QLabel("Nome:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Qtd:"))
        form_layout.addWidget(self.quantity_input)
        form_layout.addWidget(QLabel("Preço:"))
        form_layout.addWidget(self.price_input)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Adicionar")
        self.edit_btn = QPushButton("Editar")
        self.delete_btn = QPushButton("Excluir")
        self.refresh_btn = QPushButton("Atualizar")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)

