from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog
)
from models import get_all_users, User, get_user_by_email, hash_password, get_connection


class UserDialog(QDialog):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.setWindowTitle("Gerenciar Usuários")
        self.resize(600, 400)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefone", "Tipo"])

        # Botões
        self.btn_add = QPushButton("Adicionar Usuário")
        self.btn_delete = QPushButton("Excluir Usuário")

        self.btn_add.clicked.connect(self.add_user)
        self.btn_delete.clicked.connect(self.delete_user)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_delete)
        self.setLayout(layout)

        self.load_users()
        self.adjust_permissions()

    # =========================
    # 🔒 Controle de permissão
    # =========================
    def adjust_permissions(self):
        user_type = self.user_info[5]
        if user_type not in ["ADMIN", "MOD"]:
            # apenas admin e mod podem editar usuários
            self.btn_add.setEnabled(False)
            self.btn_delete.setEnabled(False)
            QMessageBox.warning(self, "Acesso Negado", "Você não tem permissão para gerenciar usuários.")
            self.close()

    # =========================
    # 👤 CRUD Usuários
    # =========================
    def load_users(self):
        users = get_all_users()
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            for col, value in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_user(self):
        name, ok = QInputDialog.getText(self, "Novo Usuário", "Nome:")
        if not ok or not name.strip():
            return

        email, ok = QInputDialog.getText(self, "Novo Usuário", "Email:")
        if not ok or not email.strip():
            return

        phone, ok = QInputDialog.getText(self, "Novo Usuário", "Telefone:")
        if not ok:
            phone = ""

        password, ok = QInputDialog.getText(self, "Novo Usuário", "Senha:")
        if not ok or not password.strip():
            return

        tipo, ok = QInputDialog.getItem(self, "Tipo de Usuário", "Escolha:", ["ADMIN", "MOD", "LIMITADO"], 0, False)
        if not ok:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM user_types WHERE name = ?", (tipo,))
        user_type_id = cur.fetchone()[0]
        conn.close()

        User.create(name, email, phone, password, user_type_id)
        self.load_users()

    def delete_user(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um usuário para excluir.")
            return

        user_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Confirmação", "Tem certeza que deseja excluir este usuário?")

        if confirm == QMessageBox.Yes:
            User.delete(user_id)
            self.load_users()
