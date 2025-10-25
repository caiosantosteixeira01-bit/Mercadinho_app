# ui/user_dialog.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog
from models import User

class UserDialog(QWidget):
    def __init__(self, logged_user):
        super().__init__()
        self.setWindowTitle("Gerenciar Usuários")
        self.setFixedSize(600, 400)
        self.logged_user = logged_user  # (id, name, email, type_name)
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefone", "Tipo", "Online"])
        layout.addWidget(self.table)

        self.add_btn = QPushButton("Adicionar Usuário")
        self.add_btn.clicked.connect(self.add_user)
        layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Editar Usuário")
        self.edit_btn.clicked.connect(self.edit_user)
        layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Deletar Usuário")
        self.delete_btn.clicked.connect(self.delete_user)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

    def load_users(self):
        self.table.setRowCount(0)
        users = User.get_all()
        for row_num, user in enumerate(users):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(user):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def add_user(self):
        tipos = ["ADMIN", "MOD", "LIMITADO"]
        if self.logged_user[3] == "MOD":
            tipos = ["LIMITADO"]

        tipo, ok = QInputDialog.getItem(self, "Tipo de Usuário", "Escolha o tipo:", tipos, 0, False)
        if ok:
            nome, ok1 = QInputDialog.getText(self, "Nome", "Nome do usuário:")
            if not ok1 or not nome: return
            email, ok2 = QInputDialog.getText(self, "Email", "Email do usuário:")
            if not ok2 or not email: return
            telefone, ok3 = QInputDialog.getText(self, "Telefone", "Telefone do usuário:")
            if not ok3: telefone = ""
            senha, ok4 = QInputDialog.getText(self, "Senha", "Senha do usuário:")
            if not ok4 or not senha: return

            user_type_id = {"ADMIN": 1, "MOD": 2, "LIMITADO": 3}[tipo]
            User.create(nome, email, telefone, senha, user_type_id)
            self.load_users()
            QMessageBox.information(self, "Sucesso", "Usuário adicionado com sucesso!")

    def edit_user(self):
        row = self.table.currentRow()
        if row < 0: 
            QMessageBox.warning(self, "Erro", "Selecione um usuário para editar")
            return

        user_id = int(self.table.item(row, 0).text())
        user_tipo = self.table.item(row, 4).text()

        # Regras de permissão
        if self.logged_user[3] == "MOD" and user_tipo != "LIMITADO":
            QMessageBox.warning(self, "Erro", "Moderadores só podem editar usuários LIMITADO")
            return
        if int(self.logged_user[0]) == user_id:
            QMessageBox.warning(self, "Erro", "Você não pode editar a si mesmo!")
            return

        # Nome
        nome, ok1 = QInputDialog.getText(self, "Nome", "Nome do usuário:", text=self.table.item(row,1).text())
        if not ok1 or not nome: return

        # Email
        email, ok2 = QInputDialog.getText(self, "Email", "Email do usuário:", text=self.table.item(row,2).text())
        if not ok2 or not email: return

        # Telefone
        telefone, ok3 = QInputDialog.getText(self, "Telefone", "Telefone do usuário:", text=self.table.item(row,3).text())
        if not ok3: telefone = ""

        # Senha
        senha, ok4 = QInputDialog.getText(self, "Senha", "Senha do usuário:")
        if not ok4 or not senha: return

        # Tipo
        tipos = ["ADMIN", "MOD", "LIMITADO"]
        if self.logged_user[3] == "MOD":
            tipos = ["LIMITADO"]
        tipo, ok5 = QInputDialog.getItem(self, "Tipo de Usuário", "Escolha o tipo:", tipos, 0, False)
        if not ok5: return
        user_type_id = {"ADMIN":1,"MOD":2,"LIMITADO":3}[tipo]

        # Atualiza no banco
        User.update(user_id, nome, email, telefone, senha, user_type_id)
        self.load_users()
        QMessageBox.information(self, "Sucesso", "Usuário atualizado com sucesso!")

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0: return
        user_id = int(self.table.item(row, 0).text())
        if int(self.logged_user[0]) == user_id:
            QMessageBox.warning(self, "Erro", "Você não pode deletar a si mesmo!")
            return
        User.delete(user_id)
        self.load_users()
        QMessageBox.information(self, "Sucesso", "Usuário deletado!")
