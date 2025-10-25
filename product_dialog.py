from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QMessageBox
from models import Product

class ProductDialog(QWidget):
    def __init__(self, logged_user):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Estoque")
        self.setFixedSize(700, 400)
        self.logged_user = logged_user  # (id, name, email, type_name)
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Categoria", "Quantidade", "Preço Compra", "Preço Venda"])
        layout.addWidget(self.table)

        self.add_btn = QPushButton("Adicionar Produto")
        self.add_btn.clicked.connect(self.add_product)
        layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Editar Produto")
        self.edit_btn.clicked.connect(self.edit_product)
        layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Deletar Produto")
        self.delete_btn.clicked.connect(self.delete_product)
        layout.addWidget(self.delete_btn)

        # Controle de permissões
        if self.logged_user[3] == "LIMITADO":
            self.add_btn.setEnabled(False)
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
        elif self.logged_user[3] == "MOD":
            self.delete_btn.setEnabled(False)  # Moderador não pode deletar

        self.setLayout(layout)

    def load_products(self):
        self.table.setRowCount(0)
        products = Product.get_all()
        for row_num, p in enumerate(products):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(p):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def add_product(self):
        name, ok1 = QInputDialog.getText(self, "Nome", "Nome do produto:")
        if not ok1 or not name: return
        category, ok2 = QInputDialog.getText(self, "Categoria", "Categoria:")
        if not ok2: category = ""
        quantity, ok3 = QInputDialog.getInt(self, "Quantidade", "Quantidade inicial:", 0, 0)
        price_purchase, ok4 = QInputDialog.getDouble(self, "Preço de Compra", "Preço de Compra:", 0.0, 0.0)
        price_sale, ok5 = QInputDialog.getDouble(self, "Preço de Venda", "Preço de Venda:", 0.0, 0.0)

        Product.create(name, category, quantity, price_purchase, price_sale)
        self.load_products()
        QMessageBox.information(self, "Sucesso", "Produto adicionado!")

    def edit_product(self):
        row = self.table.currentRow()
        if row < 0: return
        product_id = int(self.table.item(row, 0).text())

        name, ok1 = QInputDialog.getText(self, "Nome", "Nome do produto:", text=self.table.item(row,1).text())
        if not ok1 or not name: return
        category, ok2 = QInputDialog.getText(self, "Categoria", "Categoria:", text=self.table.item(row,2).text())
        if not ok2: category = ""
        quantity, ok3 = QInputDialog.getInt(self, "Quantidade", "Quantidade:", int(self.table.item(row,3).text()), 0)
        price_purchase, ok4 = QInputDialog.getDouble(self, "Preço de Compra", "Preço de Compra:", float(self.table.item(row,4).text()), 0.0)
        price_sale, ok5 = QInputDialog.getDouble(self, "Preço de Venda", "Preço de Venda:", float(self.table.item(row,5).text()), 0.0)

        Product.update(product_id, name, category, quantity, price_purchase, price_sale)
        self.load_products()
        QMessageBox.information(self, "Sucesso", "Produto atualizado!")

    def delete_product(self):
        row = self.table.currentRow()
        if row < 0: return
        product_id = int(self.table.item(row,0).text())
        Product.delete(product_id)
        self.load_products()
        QMessageBox.information(self, "Sucesso", "Produto deletado!")
