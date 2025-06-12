from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
)
from PyQt6.QtCore import Qt
import sys

from ui.formulario_asistencia import FormularioAsistencia
from ui.historial_asistencias import HistorialAsistencias
from ui.exportar_excel import ExportarExcel  # ✅ Importación del exportador

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Asistencias - DORCI")
        self.setGeometry(100, 100, 600, 450)
        self.init_ui()

    def init_ui(self):
        titulo = QLabel("📝 Sistema de Control de Asistencias")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Botones principales
        btn_registrar = QPushButton("Registrar Asistencia")
        btn_historial = QPushButton("Ver Historial")
        btn_exportar = QPushButton("Exportar a Excel")
        btn_salir = QPushButton("Salir")

        # Estilos
        estilo = "padding: 10px; font-size: 16px;"
        btn_registrar.setStyleSheet(estilo)
        btn_historial.setStyleSheet(estilo)
        btn_exportar.setStyleSheet(estilo + "background-color: #5cb85c; color: white;")
        btn_salir.setStyleSheet(estilo + "background-color: #d9534f; color: white;")

        # Conexiones
        btn_registrar.clicked.connect(self.abrir_formulario_asistencia)
        btn_historial.clicked.connect(self.abrir_historial)
        btn_exportar.clicked.connect(self.abrir_exportador)
        btn_salir.clicked.connect(self.close)

        # Layout
        layout_botones = QVBoxLayout()
        layout_botones.addWidget(btn_registrar)
        layout_botones.addWidget(btn_historial)
        layout_botones.addWidget(btn_exportar)
        layout_botones.addWidget(btn_salir)
        layout_botones.setSpacing(15)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(titulo)
        layout_principal.addLayout(layout_botones)
        layout_principal.setContentsMargins(100, 50, 100, 50)

        self.setLayout(layout_principal)

    # Funciones de apertura de ventanas
    def abrir_formulario_asistencia(self):
        formulario = FormularioAsistencia()
        formulario.exec()

    def abrir_historial(self):
        historial = HistorialAsistencias()
        historial.exec()

    def abrir_exportador(self):
        exportar = ExportarExcel()
        exportar.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
