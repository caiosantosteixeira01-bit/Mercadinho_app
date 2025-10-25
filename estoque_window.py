from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QComboBox
)
import sqlite3

class EstoqueWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Gerenciamento de Estoque")
        self.setGeometry(200, 200, 800, 450)
        self.init_ui()
        self.load_data()
        self.apply_permissions()

    def init_ui(self):
        layout = QVBoxLayout()

        # 🔍 Barra de busca e filtro
        filtro_layout = QHBoxLayout()
        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText("Buscar por nome...")

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItem("Todas as categorias")
        self.load_categorias()  # carrega categorias do banco

        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.clicked.connect(self.filtrar_dados)

        filtro_layout.addWidget(QLabel("Busca:"))
        filtro_layout.addWidget(self.input_busca)
        filtro_layout.addWidget(QLabel("Categoria:"))
        filtro_layout.addWidget(self.combo_categoria)
        filtro_layout.addWidget(self.btn_filtrar)
        layout.addLayout(filtro_layout)

        # 🧾 Tabela de produtos
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Quantidade", "Preço", "Categoria"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # 🧱 Campos de edição
        form = QHBoxLayout()
        self.nome = QLineEdit(); self.nome.setPlaceholderText("Nome")
        self.quantidade = QLineEdit(); self.quantidade.setPlaceholderText("Quantidade")
        self.preco = QLineEdit(); self.preco.setPlaceholderText("Preço")
        self.categoria = QLineEdit(); self.categoria.setPlaceholderText("Categoria")
        form.addWidget(self.nome)
        form.addWidget(self.quantidade)
        form.addWidget(self.preco)
        form.addWidget(self.categoria)
        layout.addLayout(form)

        # 🛠️ Botões de ação
        botoes = QHBoxLayout()
        self.btn_add = QPushButton("Adicionar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Excluir")
        self.btn_refresh = QPushButton("Atualizar")

        self.btn_add.clicked.connect(self.add_item)
        self.btn_edit.clicked.connect(self.edit_item)
        self.btn_delete.clicked.connect(self.delete_item)
        self.btn_refresh.clicked.connect(self.load_data)

        botoes.addWidget(self.btn_add)
        botoes.addWidget(self.btn_edit)
        botoes.addWidget(self.btn_delete)
        botoes.addWidget(self.btn_refresh)
        layout.addLayout(botoes)

        self.setLayout(layout)

    # 🧩 Aplica permissões
    def apply_permissions(self):
        tipo = self.user['tipo']
        if tipo == 'limitado':
            self.btn_add.setDisabled(True)
            self.btn_edit.setDisabled(True)
            self.btn_delete.setDisabled(True)
        elif tipo == 'mod':
            self.btn_delete.setDisabled(True)

    # 📦 Carrega dados da tabela
    def load_data(self, filtro_nome=None, filtro_categoria=None):
        conn = sqlite3.connect("mercadinho.db")
        cursor = conn.cursor()

        query = "SELECT * FROM estoque"
        params = []

        if filtro_nome or (filtro_categoria and filtro_categoria != "Todas as categorias"):
            query += " WHERE"
            condicoes = []
            if filtro_nome:
                condicoes.append(" nome LIKE ? ")
                params.append(f"%{filtro_nome}%")
            if filtro_categoria and filtro_categoria != "Todas as categorias":
                condicoes.append(" categoria = ? ")
                params.append(filtro_categoria)
            query += " AND ".join(condicoes)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    # 🔎 Filtro de dados
    def filtrar_dados(self):
        nome = self.input_busca.text()
        categoria = self.combo_categoria.currentText()
        self.load_data(nome, categoria)

    # 📚 Atualiza combo de categorias
    def load_categorias(self):
        conn = sqlite3.connect("mercadinho.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT categoria FROM estoque WHERE categoria IS NOT NULL AND categoria != ''")
        categorias = cursor.fetchall()
        conn.close()

        for c in categorias:
            self.combo_categoria.addItem(c[0])

    # ➕ Adicionar item
    def add_item(self):
        nome = self.nome.text()
        quantidade = self.quantidade.text()
        preco = self.preco.text()
        categoria = self.categoria.text()

        if not nome or not quantidade or not preco:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        conn = sqlite3.connect("mercadinho.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO estoque (nome, quantidade, preco, categoria) VALUES (?, ?, ?, ?)",
                       (nome, quantidade, preco, categoria))
        conn.commit()
        conn.close()

        self.load_categorias()  # recarrega categorias
        self.load_data()

    # ✏️ Editar item
    def edit_item(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Erro", "Selecione um item para editar!")
            return

        id_item = self.table.item(selected, 0).text()
        nome = self.nome.text()
        quantidade = self.quantidade.text()
        preco = self.preco.text()
        categoria = self.categoria.text()

        conn = sqlite3.connect("mercadinho.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE estoque SET nome=?, quantidade=?, preco=?, categoria=? WHERE id=?",
                       (nome, quantidade, preco, categoria, id_item))
        conn.commit()
        conn.close()
        self.load_data()

    # ❌ Deletar item
    def delete_item(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Erro", "Selecione um item para excluir!")
            return

        id_item = self.table.item(selected, 0).text()
        conn = sqlite3.connect("mercadinho.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estoque WHERE id=?", (id_item,))
        conn.commit()
        conn.close()
        self.load_data()
