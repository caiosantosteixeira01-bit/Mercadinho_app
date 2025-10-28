from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QAction
from ui.user_dialog import UserDialog
from auth import current_user

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mercadinho App - Painel Principal")
        self.setGeometry(300,200,900,600)

        menubar = self.menuBar()

        self.user_menu = menubar.addMenu("Usuários")
        user_create = QAction("Gerenciar Usuários",self)
        user_create.triggered.connect(self.open_user_dialog)
        self.user_menu.addAction(user_create)

        self.product_menu = menubar.addMenu("Estoque")
        from ui.product_dialog import ProductDialog
        product_manage = QAction("Gerenciar Produtos",self)
        product_manage.triggered.connect(self.open_product_dialog)
        self.product_menu.addAction(product_manage)

        if current_user["type"]=="Limitado":
            self.user_menu.menuAction().setVisible(False)

    def open_user_dialog(self):
        if current_user["type"]=="Limitado":
            QMessageBox.warning(self,"Acesso negado","Você não tem permissão para gerenciar usuários.")
            return
        dialog = UserDialog()
        dialog.exec()

    def open_product_dialog(self):
        from ui.product_dialog import ProductDialog
        dialog = ProductDialog()
        dialog.exec()
