import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class RegistroScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registro de Ponto")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel("Registro de Ponto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        self.funcionario_combo = QComboBox()
        self.funcionario_combo.setStyleSheet("""
            background-color: #1E1E1E;
            color: white;
            padding: 8px;
            font-size: 16px;
            border: 1px solid #333;
            border-radius: 8px;
        """)
        layout.addWidget(self.funcionario_combo)

        botao_entrada = QPushButton("Registrar Entrada")
        botao_saida = QPushButton("Registrar Saída")
        botao_voltar = QPushButton("Voltar")

        for botao in [botao_entrada, botao_saida, botao_voltar]:
            botao.setFixedHeight(45)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 14px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            layout.addWidget(botao)

        botao_entrada.clicked.connect(self.registrar_entrada)
        botao_saida.clicked.connect(self.registrar_saida)
        botao_voltar.clicked.connect(self.close)

        self.setLayout(layout)
        self.carregar_funcionarios()

    def carregar_funcionarios(self):
        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome FROM pessoas")
        funcionarios = cursor.fetchall()

        self.funcionario_combo.clear()
        for id_func, nome in funcionarios:
            self.funcionario_combo.addItem(f"{id_func} - {nome}")

        conexao.close()

    # Função para registrar log
    def registrar_log(self, pessoa_id, nome_funcionario, acao):
        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        cursor.execute('''
            INSERT INTO logs (pessoa_id, nome_funcionario, acao)
            VALUES (?, ?, ?)
        ''', (pessoa_id, nome_funcionario, acao))

        conexao.commit()
        conexao.close()

    def registrar_entrada(self):
        funcionario = self.funcionario_combo.currentText()
        if not funcionario:
            QMessageBox.warning(self, "Erro", "Selecione um funcionário!")
            return

        pessoa_id, nome = funcionario.split(" - ")[0], funcionario.split(" - ")[1]

        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        hoje = datetime.now().strftime("%Y-%m-%d")

        cursor.execute('''
            SELECT entrada FROM registros
            WHERE pessoa_id = ? AND DATE(entrada) = ? AND saida IS NULL
        ''', (pessoa_id, hoje))
        registro = cursor.fetchone()

        if registro:
            QMessageBox.warning(self, "Erro", "Já existe uma entrada hoje sem saída!")
        else:
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO registros (pessoa_id, entrada)
                VALUES (?, ?)
            ''', (pessoa_id, agora))

            conexao.commit()
            self.registrar_log(pessoa_id, nome, "Registrou Entrada")
            QMessageBox.information(self, "Sucesso", f"Entrada registrada às {agora}!")

        conexao.close()

    def registrar_saida(self):
        funcionario = self.funcionario_combo.currentText()
        if not funcionario:
            QMessageBox.warning(self, "Erro", "Selecione um funcionário!")
            return

        pessoa_id, nome = funcionario.split(" - ")[0], funcionario.split(" - ")[1]

        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT id FROM registros
            WHERE pessoa_id = ? AND saida IS NULL
            ORDER BY entrada DESC
            LIMIT 1
        ''', (pessoa_id,))
        registro = cursor.fetchone()

        if not registro:
            QMessageBox.warning(self, "Erro", "Nenhuma entrada aberta para fechar com saída!")
        else:
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            registro_id = registro[0]

            cursor.execute('''
                UPDATE registros
                SET saida = ?
                WHERE id = ?
            ''', (agora, registro_id))

            conexao.commit()
            self.registrar_log(pessoa_id, nome, "Registrou Saída")
            QMessageBox.information(self, "Sucesso", f"Saída registrada às {agora}!")

        conexao.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistroScreen()
    window.show()
    sys.exit(app.exec_())
