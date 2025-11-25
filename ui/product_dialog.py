from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout
from models import get_all_products, Product

class ProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Produtos")
        self.resize(600, 300)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.refresh_table()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome")
        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Qtd")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Preço")

        add_btn = QPushButton("Adicionar")
        add_btn.clicked.connect(self.add_product)

        delete_btn = QPushButton("Excluir")
        delete_btn.clicked.connect(self.delete_product)

        h = QHBoxLayout()
        h.addWidget(self.name_input)
        h.addWidget(self.qty_input)
        h.addWidget(self.price_input)
        h.addWidget(add_btn)
        h.addWidget(delete_btn)

        layout.addWidget(self.table)
        layout.addLayout(h)
        self.setLayout(layout)

    def refresh_table(self):
        data = get_all_products()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Qtd", "Preço"])
        for row, p in enumerate(data):
            for col, val in enumerate(p):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))

    def add_product(self):
        name = self.name_input.text().strip()
        qty = int(self.qty_input.text() or 0)
        price = float(self.price_input.text() or 0)
        if name:
            Product.create(name, qty, price)
            self.refresh_table()

    def delete_product(self):
        row = self.table.currentRow()
        if row < 0:
            return
        pid = int(self.table.item(row, 0).text())
        Product.delete(pid)
        self.refresh_table()
