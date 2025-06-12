from PyQt6.QtWidgets import QApplication
import sys
from ui.ventana_principal import VentanaPrincipal
from db.conexion import obtener_conexion

if __name__ == "__main__":
    db = obtener_conexion()
    if db:
        app = QApplication(sys.argv)
        ventana = VentanaPrincipal()
        import qdarkstyle
app.setStyleSheet(qdarkstyle.load_stylesheet())
        ventana.show()
        sys.exit(app.exec())
    else:
        print("Error al iniciar la aplicación. Verifica la conexión con MongoDB.")
