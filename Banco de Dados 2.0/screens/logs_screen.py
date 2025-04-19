import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class LogsScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logs do Sistema")
        self.setGeometry(100, 100, 700, 700)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel("Histórico de Atividades")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        self.logs_area = QTextEdit()
        self.logs_area.setReadOnly(True)
        self.logs_area.setStyleSheet("""
            background-color: #1E1E1E;
            color: white;
            font-size: 14px;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 8px;
        """)
        layout.addWidget(self.logs_area)

        botao_atualizar = QPushButton("Atualizar Logs")
        botao_atualizar.setFixedHeight(45)
        botao_atualizar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        botao_atualizar.clicked.connect(self.carregar_logs)
        layout.addWidget(botao_atualizar)

        self.setLayout(layout)
        self.carregar_logs()

    def carregar_logs(self):
        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT data_hora, nome_funcionario, acao
            FROM logs
            ORDER BY data_hora DESC
        ''')
        logs = cursor.fetchall()
        conexao.close()

        texto_logs = ""
        for data_hora, nome, acao in logs:
            texto_logs += f"🕒 {data_hora} | 👤 {nome} | 📝 {acao}\n"

        self.logs_area.setText(texto_logs)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LogsScreen()
    window.show()
    sys.exit(app.exec_())
