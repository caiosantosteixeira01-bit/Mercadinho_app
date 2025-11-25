from PyQt5.QtWidgets import (
    QMainWindow, QAction, QMessageBox, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QWidget
)
from ui.product_dialog import ProductDialog
from ui.user_dialog import UserDialog
from models import get_all_products, Product


class MainWindow(QMainWindow):
    def __init__(self, user_info):
        super().__init__()

        # user_info = (id, name, email, phone, password, tipo_nome)
        self.user_id = user_info[0]
        self.user_name = user_info[1]
        self.user_email = user_info[2]
        self.user_phone = user_info[3]
        self.user_password = user_info[4]
        self.user_type = user_info[5]   # Agora vem como string: ADMIN, MOD, LIMITADO

        self.setWindowTitle(f"Mercadinho - Sistema de Estoque ({self.user_type})")
        self.resize(800, 600)

        self.create_menus()

        self.table = QTableWidget()
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

        self.load_products()
        self.adjust_permissions()

    def create_menus(self):
        menubar = self.menuBar()

        self.user_menu = menubar.addMenu("Usuários")
        action = QAction("Gerenciar Usuários", self)
        action.triggered.connect(self.open_user_dialog)
        self.user_menu.addAction(action)

        stock_menu = menubar.addMenu("Estoque")
        reload_action = QAction("Recarregar", self)
        reload_action.triggered.connect(self.load_products)
        stock_menu.addAction(reload_action)

    def adjust_permissions(self):
        """
        ADMIN  → pode tudo
        MOD    → pode tudo, menos ver usuários
        LIMITADO → não pode nada além de visualizar
        """

        if self.user_type == "LIMITADO":
            self.btn_add.setEnabled(False)
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)

        # Ocultar menu de usuários para quem não é ADMIN
        if self.user_type != "ADMIN":
            self.user_menu.menuAction().setVisible(False)

    def load_products(self):
        products = get_all_products()
        self.table.setRowCount(len(products))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Preço", "Estoque"])

        for r, product in enumerate(products):
            for c, value in enumerate(product):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def add_product(self):
        dlg = ProductDialog()
        if dlg.exec_():
            name, price, stock = dlg.get_data()
            Product.create(name, price, stock)
            self.load_products()

    def edit_product(self):
        row = self.table.currentRow()
        if row == -1:
            return QMessageBox.warning(self, "Aviso", "Selecione um produto.")

        product_id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        price = float(self.table.item(row, 2).text())
        stock = int(self.table.item(row, 3).text())

        dlg = ProductDialog(name, price, stock)
        if dlg.exec_():
            new_name, new_price, new_stock = dlg.get_data()
            Product.update(product_id, new_name, new_price, new_stock)
            self.load_products()

    def delete_product(self):
        row = self.table.currentRow()
        if row == -1:
            return QMessageBox.warning(self, "Aviso", "Selecione um produto.")

        if QMessageBox.question(self, "Confirmação", "Excluir?") == QMessageBox.Yes:
            product_id = int(self.table.item(row, 0).text())
            Product.delete(product_id)
            self.load_products()

    def open_user_dialog(self):
        dlg = UserDialog(self.user_type)
        dlg.exec_()
