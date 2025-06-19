# ubicacion: asistencia_dorci/main.py

import sys
from PyQt6.QtWidgets import QApplication
# --- NUEVA IMPORTACIÓN PARA EL IDIOMA ---
from PyQt6.QtCore import QLocale
# ------------------------------------
from ui.login import LoginVentana
from ui.ventana_principal import VentanaPrincipal

def load_stylesheet(filepath):
    """Función para cargar una hoja de estilos desde un archivo."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo de estilos en {filepath}")
        return ""

def main():
    app = QApplication(sys.argv)

    # --- ESTABLECEMOS EL IDIOMA PREDETERMINADO A ESPAÑOL ---
    QLocale.setDefault(QLocale(QLocale.Language.Spanish))
    # ----------------------------------------------------

    app.setStyleSheet(load_stylesheet("ui/styles.qss"))
    
    exit_code = 123 
    
    while exit_code == 123:
        login = LoginVentana()
        
        if login.exec():
            window = VentanaPrincipal(login.user_rol)
            window.showMaximized()
            exit_code = app.exec()
        else:
            exit_code = 0
            
if __name__ == "__main__":
    main()