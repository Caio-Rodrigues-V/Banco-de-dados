import sys
from PyQt5.QtWidgets import QApplication
from screens.splash_screen import SplashScreen
from screens.login_screen import LoginScreen
import shutil
import threading
import time
from datetime import datetime
import os
 
def agendar_backup():
    while True:
        agora = datetime.now()
        if agora.hour == 22 and agora.minute == 0:  # Quando der 22h00
            try:
                if not os.path.exists('backups'):
                    os.makedirs('backups')

                horario_formatado = agora.strftime("%Y-%m-%d_%H-%M-%S")
                shutil.copy('database/empresa.db', f'backups/backup_{horario_formatado}.db')
                print(f"[BACKUP] Backup realizado às {horario_formatado}")
                time.sleep(60)  # Espera 1 minuto pra não fazer backup múltiplo
            except Exception as e:
                print(f"[ERRO NO BACKUP] {e}")
        time.sleep(30)  # Checa a cada 30 segundos

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Iniciar thread do backup
    thread_backup = threading.Thread(target=agendar_backup)
    thread_backup.daemon = True
    thread_backup.start()

    splash = SplashScreen()
    splash.show()

    def abrir_login():
        splash.close()
        app.login = LoginScreen()
        app.login.show()

    splash.iniciar(abrir_login)

    sys.exit(app.exec_())