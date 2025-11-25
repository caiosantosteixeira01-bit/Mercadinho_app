from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog
)
from models import get_all_users, User, get_connection


class UserDialog(QDialog):
    def __init__(self, user_type):
        super().__init__()

        # Agora user_type é: "ADMIN", "MOD" ou "LIMITADO"
        self.user_type = user_type

        self.setWindowTitle("Gerenciar Usuários")
        self.resize(600, 400)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nome", "Email", "Telefone", "Tipo"]
        )

        self.btn_add = QPushButton("Adicionar Usuário")
        self.btn_delete = QPushButton("Excluir Usuário")

        self.btn_add.clicked.connect(self.add_user)
        self.btn_delete.clicked.connect(self.delete_user)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_delete)
        self.setLayout(layout)

        self.adjust_permissions()
        self.load_users()

    def adjust_permissions(self):
        # Somente ADMIN pode acessar
        if self.user_type != "ADMIN":
            QMessageBox.warning(self, "Acesso Negado", "Apenas administradores podem acessar.")
            self.close()

    def load_users(self):
        users = get_all_users()
        self.table.setRowCount(len(users))

        for r, user in enumerate(users):
            for c, val in enumerate(user):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def add_user(self):
        name, ok = QInputDialog.getText(self, "Nome", "Nome:")
        if not ok or not name:
            return

        email, ok = QInputDialog.getText(self, "Email", "Email:")
        if not ok or not email:
            return

        phone, ok = QInputDialog.getText(self, "Telefone", "Telefone:")
        if not ok:
            return

        password, ok = QInputDialog.getText(self, "Senha", "Senha:")
        if not ok or not password:
            return

        tipo, ok = QInputDialog.getItem(
            self, "Tipo", "Escolha:", ["ADMIN", "MOD", "LIMITADO"], 0, False
        )
        if not ok:
            return

        # Buscar ID da tabela user_types
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM user_types WHERE name = ?", (tipo,))
        result = cur.fetchone()
        conn.close()

        if not result:
            QMessageBox.warning(self, "Erro", "Tipo de usuário inválido no banco.")
            return

        type_id = result[0]

        User.create(name, email, phone, password, type_id)
        self.load_users()

    def delete_user(self):
        row = self.table.currentRow()
        if row == -1:
            return QMessageBox.warning(self, "Aviso", "Selecione um usuário.")

        user_id = int(self.table.item(row, 0).text())
        tipo_usuario = self.table.item(row, 4).text()

        # ADMIN não pode excluir outro ADMIN
        if tipo_usuario == "ADMIN":
            return QMessageBox.warning(self, "Ação Bloqueada", "Não é permitido excluir administradores.")

        if QMessageBox.question(self, "Confirmação", "Excluir este usuário?") == QMessageBox.Yes:
            User.delete(user_id)
            self.load_users()
