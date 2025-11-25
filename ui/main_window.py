from PyQt5.QtWidgets import (
    QMainWindow, QAction, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
)
from ui.product_dialog import ProductDialog
from ui.user_dialog import UserDialog
from models import get_all_products, Product


class MainWindow(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info  # (id, nome, email, telefone, senha, tipo)
        self.setWindowTitle("Mercadinho - Sistema de Estoque")
        self.resize(800, 600)

        # Cria menu
        self.create_menus()

        # Cria a tabela principal
        self.table = QTableWidget()
        self.setCentralWidget(self.table)
        self.load_products()

        # Botões CRUD de produtos
        self.btn_add = QPushButton("Adicionar Produto")
        self.btn_edit = QPushButton("Editar Produto")
        self.btn_delete = QPushButton("Remover Produto")

        self.btn_add.clicked.connect(self.add_product)
        self.btn_edit.clicked.connect(self.edit_product)
        self.btn_delete.clicked.connect(self.delete_product)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Ajusta permissões conforme tipo do usuário
        self.adjust_permissions()

    # =========================
    # 🎛️ Menu superior
    # =========================
    def create_menus(self):
        menubar = self.menuBar()

        # Menu Usuários (somente Admin e Mod)
        self.user_menu = menubar.addMenu("Usuários")
        self.manage_users_action = QAction("Gerenciar Usuários", self)
        self.manage_users_action.triggered.connect(self.open_user_dialog)
        self.user_menu.addAction(self.manage_users_action)

        # Menu Estoque (todos)
        self.stock_menu = menubar.addMenu("Estoque")
        self.reload_action = QAction("Recarregar", self)
        self.reload_action.triggered.connect(self.load_products)
        self.stock_menu.addAction(self.reload_action)

    # =========================
    # 🔒 Permissões por tipo
    # =========================
    def adjust_permissions(self):
        """Controla permissões com base no tipo de usuário."""
        # Detecta se é dicionário ou tupla
        user_type = None
        if isinstance(self.user_info, dict):
            user_type = self.user_info.get("type")
        elif isinstance(self.user_info, (list, tuple)):
            user_type = self.user_info[5]  # tipo na posição 5

        # Desativa recursos conforme o tipo
        if user_type == "LIMITADO":
            self.btn_add_user.setEnabled(False)
            self.btn_edit_user.setEnabled(False)
            self.btn_delete_user.setEnabled(False)
            self.tab_users.setEnabled(False)
        elif user_type == "MOD":
            self.btn_delete_user.setEnabled(False)

    # =========================
    # 📦 Produtos
    # =========================
    def load_products(self):
        products = get_all_products()
        self.table.setRowCount(len(products))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Preço", "Estoque"])

        for row, product in enumerate(products):
            for col, value in enumerate(product):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_product(self):
        dialog = ProductDialog()
        if dialog.exec_():
            name, price, stock = dialog.get_data()
            Product.create(name, price, stock)
            self.load_products()

    def edit_product(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para editar.")
            return

        product_id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        price = float(self.table.item(row, 2).text())
        stock = int(self.table.item(row, 3).text())

        dialog = ProductDialog(name, price, stock)
        if dialog.exec_():
            new_name, new_price, new_stock = dialog.get_data()
            Product.update(product_id, new_name, new_price, new_stock)
            self.load_products()

    def delete_product(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para remover.")
            return

        product_id = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(self, "Confirmação", "Deseja excluir este produto?")
        if confirm == QMessageBox.Yes:
            Product.delete(product_id)
            self.load_products()

    # =========================
    # 👥 Gerenciamento de usuários
    # =========================
    def open_user_dialog(self):
        dialog = UserDialog(self.user_info)
        dialog.exec_()
