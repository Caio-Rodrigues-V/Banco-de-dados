import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QMessageBox, QCalendarWidget, QTimeEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QDate, QTime

class RegistroManualScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registro Manual de Ponto")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel("Registro Manual de Ponto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        self.funcionario_combo = QComboBox()
        self.funcionario_combo.setStyleSheet(self.estilo_input())
        layout.addWidget(self.funcionario_combo)

        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.calendario.setStyleSheet(self.estilo_calendario())
        layout.addWidget(self.calendario)

        self.entrada_time = QTimeEdit()
        self.entrada_time.setDisplayFormat("HH:mm")
        self.entrada_time.setStyleSheet(self.estilo_input())
        layout.addWidget(self.entrada_time)

        self.saida_time = QTimeEdit()
        self.saida_time.setDisplayFormat("HH:mm")
        self.saida_time.setStyleSheet(self.estilo_input())
        layout.addWidget(self.saida_time)

        self.botao_registrar = QPushButton("Registrar Manualmente")
        self.botao_registrar.setFixedHeight(50)
        self.botao_registrar.setStyleSheet("""
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
        self.botao_registrar.clicked.connect(self.registrar_manual)
        layout.addWidget(self.botao_registrar)

        self.setLayout(layout)
        self.carregar_funcionarios()

    def estilo_input(self):
        return """
            background-color: #1E1E1E;
            color: white;
            padding: 8px;
            font-size: 16px;
            border: 1px solid #333;
            border-radius: 8px;
        """

    def estilo_calendario(self):
        return """
            QCalendarWidget {
                background-color: #121212;
                color: white;
                border: none;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #121212;
                selection-background-color: #4CAF50;
                selection-color: black;
                font-size: 14px;
                color: white;
            }
            QCalendarWidget QToolButton {
                background-color: transparent;
                color: white;
                font-size: 16px;
                font-weight: bold;
                height: 30px;
                margin: 5px;
                border: none;
            }
            QCalendarWidget QMenu {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #4CAF50;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #121212;
            }
        """

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

    def registrar_manual(self):
        funcionario = self.funcionario_combo.currentText()
        if not funcionario:
            QMessageBox.warning(self, "Erro", "Selecione um funcionário!")
            return

        pessoa_id, nome = funcionario.split(" - ")[0], funcionario.split(" - ")[1]

        data_selecionada = self.calendario.selectedDate().toString("yyyy-MM-dd")
        hora_entrada = self.entrada_time.time().toString("HH:mm")
        hora_saida = self.saida_time.time().toString("HH:mm")

        entrada_final = f"{data_selecionada} {hora_entrada}:00"
        saida_final = f"{data_selecionada} {hora_saida}:00"

        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT entrada, saida FROM registros
            WHERE pessoa_id = ? AND DATE(entrada) = ?
        ''', (pessoa_id, data_selecionada))
        registros = cursor.fetchall()

        if registros:
            QMessageBox.warning(self, "Erro", "Já existe registro para este dia!")
            conexao.close()
            return

        cursor.execute('''
            INSERT INTO registros (pessoa_id, entrada, saida)
            VALUES (?, ?, ?)
        ''', (pessoa_id, entrada_final, saida_final))

        conexao.commit()
        self.registrar_log(pessoa_id, nome, "Registro Manual")
        conexao.close()

        QMessageBox.information(self, "Sucesso", "Registro manual feito com sucesso!")
        self.entrada_time.setTime(QTime(0, 0))
        self.saida_time.setTime(QTime(0, 0))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = RegistroManualScreen()
    window.show()
    sys.exit(app.exec_())
