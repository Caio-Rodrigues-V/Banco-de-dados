import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3

class CadastroScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cadastro de Funcionário")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)

        # Nome
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome Completo")
        self.nome_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.nome_input)

        # Cargo (ComboBox)
        self.cargo_input = QComboBox()
        self.cargo_input.addItems(["Estagiário", "Professor", "TI", "RH", "Financeiro", "Outro"])
        self.cargo_input.setStyleSheet("""
            background-color: #1E1E1E;
            color: white;
            padding: 8px;
            font-size: 16px;
            border: 1px solid #333;
            border-radius: 8px;
        """)
        layout.addWidget(self.cargo_input)

        # CPF
        self.cpf_input = QLineEdit()
        self.cpf_input.setPlaceholderText("CPF (000.000.000-00)")
        self.cpf_input.setInputMask("000.000.000-00;_")
        self.cpf_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.cpf_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.email_input)

        # Celular
        self.celular_input = QLineEdit()
        self.celular_input.setPlaceholderText("Celular (00) 00000-0000")
        self.celular_input.setInputMask("(00) 00000-0000;_")
        self.celular_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.celular_input)

        # Horário Entrada
        self.entrada_input = QLineEdit()
        self.entrada_input.setPlaceholderText("Horário Entrada (HH:MM)")
        self.entrada_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.entrada_input)

        # Horário Saída
        self.saida_input = QLineEdit()
        self.saida_input.setPlaceholderText("Horário Saída (HH:MM)")
        self.saida_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.saida_input)

        # Botão cadastrar
        self.botao_cadastrar = QPushButton("Cadastrar Funcionário")
        self.botao_cadastrar.clicked.connect(self.cadastrar_funcionario)
        self.botao_cadastrar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.botao_cadastrar)

        self.setLayout(layout)

    def estilo_input(self):
        return """
            background-color: #1E1E1E;
            color: white;
            padding: 8px;
            font-size: 16px;
            border: 1px solid #333;
            border-radius: 8px;
        """

    def cadastrar_funcionario(self):
        nome = self.nome_input.text()
        cargo = self.cargo_input.currentText()
        cpf = self.cpf_input.text()
        email = self.email_input.text()
        celular = self.celular_input.text()
        horario_entrada = self.entrada_input.text()
        horario_saida = self.saida_input.text()

        if not nome or not cpf or not email or not celular or not horario_entrada or not horario_saida:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        try:
            cursor.execute('''
                INSERT INTO pessoas (nome, cargo, cpf, email, celular, horario_entrada, horario_saida)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, cargo, cpf, email, celular, horario_entrada, horario_saida))
            
            conexao.commit()
            QMessageBox.information(self, "Sucesso", "Funcionário cadastrado com sucesso!")
            self.limpar_campos()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Erro", "CPF já cadastrado!")

        conexao.close()

    def limpar_campos(self):
        self.nome_input.clear()
        self.cargo_input.setCurrentIndex(0)
        self.cpf_input.clear()
        self.email_input.clear()
        self.celular_input.clear()
        self.entrada_input.clear()
        self.saida_input.clear()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CadastroScreen()
    window.show()
    sys.exit(app.exec_())
