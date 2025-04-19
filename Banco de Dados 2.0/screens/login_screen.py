import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from screens.dashboard import DashboardScreen  # IMPORTANTE

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Sistema de Ponto")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)

        # Título
        titulo = QLabel("Sistema de Banco de Horas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # Usuário
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Usuário")
        self.usuario_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.usuario_input)

        # Senha
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)
        self.senha_input.setStyleSheet(self.estilo_input())
        layout.addWidget(self.senha_input)

        # Botão Login
        botao_login = QPushButton("Entrar")
        botao_login.setFixedHeight(45)
        botao_login.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        botao_login.clicked.connect(self.validar_login)
        layout.addWidget(botao_login)

        self.setLayout(layout)

    def estilo_input(self):
        return """
            background-color: #1E1E1E;
            color: white;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #333;
            border-radius: 8px;
        """

    def validar_login(self):
        usuario = self.usuario_input.text()
        senha = self.senha_input.text()

        if usuario == "admin" and senha == "1234":  # <- Aqui você pode trocar o login/senha se quiser
            self.dashboard = DashboardScreen()
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos!")

    def closeEvent(self, event):
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "Sair", "Deseja realmente sair do sistema?", 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec_())
