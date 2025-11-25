from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton

class ProductDialog(QDialog):
    def __init__(self, name="", price="", stock=""):
        super().__init__()
        self.setWindowTitle("Produto")

        layout = QVBoxLayout()

        self.name = QLineEdit(name)
        self.price = QLineEdit(str(price))
        self.stock = QLineEdit(str(stock))

        self.btn_ok = QPushButton("Salvar")
        self.btn_ok.clicked.connect(self.accept)

        layout.addWidget(self.name)
        layout.addWidget(self.price)
        layout.addWidget(self.stock)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def get_data(self):
        return self.name.text(), float(self.price.text()), int(self.stock.text())
