from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from models import User, get_all_users, update_user, delete_user
from auth import current_user

class UserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Usuários")
        self.resize(700, 500)

        # 🔒 Controle de Permissões
        if current_user["type"] == "Limitado":
            QMessageBox.warning(self, "Acesso negado", "Você não tem permissão para acessar esta área.")
            self.close()
            return

        # Moderador só pode criar usuários limitados
        if current_user["type"] == "Moderador":
            self.allowed_types = ["Limitado"]
        else:
            self.allowed_types = ["Admin", "Moderador", "Limitado"]

        layout = QVBoxLayout()

        # --- Formulário ---
        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome completo")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefone")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.type_combo = QComboBox()
        self.type_combo.addItems(self.allowed_types)

        form_layout.addWidget(QLabel("Nome:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(QLabel("Telefone:"))
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(QLabel("Senha:"))
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(QLabel("Tipo:"))
        form_layout.addWidget(self.type_combo)

        layout.addLayout(form_layout)

        # --- Botões ---
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar")
        edit_btn = QPushButton("Editar")
        delete_btn = QPushButton("Excluir")
        refresh_btn = QPushButton("Atualizar")

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(refresh_btn)

        layout.addLayout(btn_layout)

        # --- Tabela ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefone", "Tipo", "Online"])
        layout.addWidget(self.table)

        self.setLayout(layout)

        # --- Eventos ---
        add_btn.clicked.connect(self.add_user)
        edit_btn.clicked.connect(self.edit_user)
        delete_btn.clicked.connect(self.delete_user)
        refresh_btn.clicked.connect(self.load_users)

        self.load_users()

    def load_users(self):
        users = get_all_users()
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            for col, data in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def add_user(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()
        user_type = self.type_combo.currentText()

        if not all([name, email, password]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios!")
            return

        # Moderador não pode criar Admin ou Moderador
        if current_user["type"] == "Moderador" and user_type != "Limitado":
            QMessageBox.warning(self, "Permissão negada", "Moderadores só podem criar usuários limitados.")
            return

        try:
            User.create(name, email, phone, password, user_type)
            QMessageBox.information(self, "Sucesso", f"Usuário {name} criado com sucesso!")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar usuário: {e}")

    def edit_user(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selecione um usuário", "Selecione um usuário para editar.")
            return

        user_id = int(self.table.item(selected, 0).text())
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()
        user_type = self.type_combo.currentText()

        selected_type = self.table.item(selected, 4).text()
        if current_user["type"] == "Moderador" and selected_type != "Limitado":
            QMessageBox.warning(self, "Permissão negada", "Você não pode editar esse tipo de usuário.")
            return

        try:
            update_user(user_id, name, email, phone, password, user_type)
            QMessageBox.information(self, "Sucesso", "Usuário atualizado com sucesso!")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar: {e}")

    def delete_user(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selecione um usuário", "Selecione um usuário para excluir.")
            return

        user_id = int(self.table.item(selected, 0).text())
        user_type = self.table.item(selected, 4).text()

        if current_user["type"] == "Moderador" and user_type != "Limitado":
            QMessageBox.warning(self, "Permissão negada", "Você não pode excluir esse tipo de usuário.")
            return

        confirm = QMessageBox.question(
            self, "Confirmação", "Deseja realmente excluir este usuário?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            delete_user(user_id)
            QMessageBox.information(self, "Sucesso", "Usuário excluído com sucesso!")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao excluir: {e}")
