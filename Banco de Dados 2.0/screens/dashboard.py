import sys
import os
import shutil
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from screens.cadastro_screen import CadastroScreen
from screens.registro_screen import RegistroScreen
from screens.registro_manual_screen import RegistroManualScreen
from screens.relatorio_screen import RelatorioScreen
from screens.logs_screen import LogsScreen

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Banco de Horas - Dashboard")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel("Sistema de Banco de Horas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # Botões
        botao_cadastro = QPushButton("➕ Cadastrar Funcionário")
        botao_registro = QPushButton("🕒 Registrar Entrada/Saída")
        botao_registro_manual = QPushButton("✍️ Registro Manual")
        botao_relatorio = QPushButton("📑 Relatório de Funcionário")
        botao_logs = QPushButton("📜 Histórico de Logs")
        botao_backup = QPushButton("💾 Gerar Backup")  # NOVO BOTÃO

        # Ajuste visual dos botões
        for botao in [botao_cadastro, botao_registro, botao_registro_manual, botao_relatorio, botao_logs, botao_backup]:
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

        # Conexões dos botões
        botao_cadastro.clicked.connect(self.abrir_cadastro)
        botao_registro.clicked.connect(self.abrir_registro)
        botao_registro_manual.clicked.connect(self.abrir_registro_manual)
        botao_relatorio.clicked.connect(self.abrir_relatorio)
        botao_logs.clicked.connect(self.abrir_logs)
        botao_backup.clicked.connect(self.gerar_backup)  # NOVO BOTÃO

        self.setLayout(layout)

    # Funções dos botões
    def abrir_cadastro(self):
        self.cadastro = CadastroScreen()
        self.cadastro.show()

    def abrir_registro(self):
        self.registro = RegistroScreen()
        self.registro.show()

    def abrir_registro_manual(self):
        self.registro_manual = RegistroManualScreen()
        self.registro_manual.show()

    def abrir_relatorio(self):
        self.relatorio = RelatorioScreen()
        self.relatorio.show()

    def abrir_logs(self):
        self.logs = LogsScreen()
        self.logs.show()

    def gerar_backup(self):
        try:
            if not os.path.exists('backups'):
                os.makedirs('backups')

            agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            shutil.copy('database/empresa.db', f'backups/backup_{agora}.db')

            QMessageBox.information(self, "Backup Realizado", f"Backup criado com sucesso em /backups/backup_{agora}.db")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o backup:\n{str(e)}")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DashboardScreen()
    window.show()
    sys.exit(app.exec_())
