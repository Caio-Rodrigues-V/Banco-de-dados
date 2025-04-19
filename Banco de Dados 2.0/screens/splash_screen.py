import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: #121212;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Logo do colégio (opcional)
        logo = QLabel()
        pixmap = QPixmap('assets/logo.png')  # coloca a imagem dentro da pasta assets
        logo.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # Texto carregando
        self.label = QLabel("Carregando Sistema...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; color: white; margin-top: 20px;")
        layout.addWidget(self.label)

        self.setLayout(layout)

    def iniciar(self, funcao_apos):
        QTimer.singleShot(3000, funcao_apos)  # Fica 3 segundos na tela
