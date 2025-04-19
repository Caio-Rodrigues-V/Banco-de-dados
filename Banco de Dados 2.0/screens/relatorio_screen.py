import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

class RelatorioScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relatório de Funcionário")
        self.setGeometry(100, 100, 700, 700)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel("Relatório de Funcionário")
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

        self.botao_gerar = QPushButton("Gerar Relatório")
        self.botao_gerar.setFixedHeight(45)
        self.botao_gerar.setStyleSheet("""
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
        self.botao_gerar.clicked.connect(self.gerar_relatorio)
        layout.addWidget(self.botao_gerar)

        self.relatorio_area = QTextEdit()
        self.relatorio_area.setReadOnly(True)
        self.relatorio_area.setStyleSheet("""
            background-color: #1E1E1E;
            color: white;
            font-size: 14px;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 8px;
        """)
        layout.addWidget(self.relatorio_area)

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

    def gerar_relatorio(self):
        funcionario = self.funcionario_combo.currentText()
        if not funcionario:
            QMessageBox.warning(self, "Erro", "Selecione um funcionário!")
            return

        pessoa_id = funcionario.split(" - ")[0]

        conexao = sqlite3.connect('database/empresa.db')
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT nome, cargo, cpf, email, celular, horario_entrada, horario_saida
            FROM pessoas
            WHERE id = ?
        ''', (pessoa_id,))
        pessoa = cursor.fetchone()

        if not pessoa:
            QMessageBox.warning(self, "Erro", "Funcionário não encontrado!")
            conexao.close()
            return

        nome, cargo, cpf, email, celular, horario_entrada_esperado, horario_saida_esperado = pessoa

        relatorio = f"🔵 Nome: {nome}\nCargo: {cargo}\nCPF: {cpf}\nEmail: {email}\nCelular: {celular}\n"
        relatorio += f"Horário Esperado: {horario_entrada_esperado} às {horario_saida_esperado}\n\n"

        # Cálculo do Saldo Total Geral
        cursor.execute('''
            SELECT entrada, saida
            FROM registros
            WHERE pessoa_id = ?
        ''', (pessoa_id,))
        registros = cursor.fetchall()

        saldo_total_minutos = 0

        for entrada_real, saida_real in registros:
            if entrada_real and saida_real:
                entrada_dt = datetime.strptime(entrada_real, "%Y-%m-%d %H:%M:%S")
                saida_dt = datetime.strptime(saida_real, "%Y-%m-%d %H:%M:%S")

                data_base = entrada_dt.strftime("%Y-%m-%d")

                entrada_esperada_dt = datetime.strptime(f"{data_base} {horario_entrada_esperado}", "%Y-%m-%d %H:%M")
                saida_esperada_dt = datetime.strptime(f"{data_base} {horario_saida_esperado}", "%Y-%m-%d %H:%M")

                trabalhado = saida_dt - entrada_dt
                esperado = saida_esperada_dt - entrada_esperada_dt

                saldo_dia = (trabalhado.total_seconds() - esperado.total_seconds()) / 60
                saldo_total_minutos += saldo_dia

        conexao.close()

        horas_total = int(abs(saldo_total_minutos) // 60)
        minutos_total = int(abs(saldo_total_minutos) % 60)

        relatorio += "📈 Banco de Horas Total:\n"
        if saldo_total_minutos > 0:
            relatorio += f"Saldo total positivo: +{horas_total}h {minutos_total}min"
        elif saldo_total_minutos < 0:
            relatorio += f"Saldo total negativo: -{horas_total}h {minutos_total}min"
        else:
            relatorio += "Saldo total zerado."

        self.relatorio_area.setText(relatorio)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = RelatorioScreen()
    window.show()
    sys.exit(app.exec_())
