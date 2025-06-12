# ui/exportar_excel.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from openpyxl import Workbook
from controllers.asistencias_controller import obtener_historial_asistencias

class ExportarExcel(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exportar a Excel")
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("📤 Exportar Historial a Excel")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")

        btn_exportar = QPushButton("Exportar ahora")
        btn_exportar.setStyleSheet("padding: 10px; font-size: 16px;")

        btn_exportar.clicked.connect(self.exportar_a_excel)

        layout.addWidget(titulo)
        layout.addWidget(btn_exportar)
        self.setLayout(layout)

    def exportar_a_excel(self):
        historial = obtener_historial_asistencias()

        if not historial:
            QMessageBox.warning(self, "Sin datos", "No hay registros para exportar.")
            return

        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar como", "historial_asistencias.xlsx", "Archivos Excel (*.xlsx)")
        if not ruta_archivo:
            return

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Asistencias"

            ws.append(["Nombre", "Cédula", "Hora Entrada", "Hora Salida", "Fecha de Registro"])
            for r in historial:
                ws.append([
                    r.get("nombre", ""),
                    r.get("cedula", ""),
                    r.get("hora_entrada", ""),
                    r.get("hora_salida", ""),
                    r.get("fecha_registro", "").strftime("%Y-%m-%d %H:%M:%S") if r.get("fecha_registro") else ""
                ])

            wb.save(ruta_archivo)
            QMessageBox.information(self, "Éxito", "El historial fue exportado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al exportar:\n{e}")
