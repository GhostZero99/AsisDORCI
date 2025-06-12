# ui/historial_asistencias.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from controllers.asistencias_controller import obtener_historial_asistencias, exportar_asistencias_a_pdf
from ui.editar_asistencia import EditarAsistencia

class HistorialAsistencias(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de Asistencias")
        self.resize(800, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        titulo = QLabel("📚 Historial de Asistencias")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        # Buscador por cédula
        buscador_layout = QHBoxLayout()
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por cédula...")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.filtrar_por_cedula)

        buscador_layout.addWidget(self.input_busqueda)
        buscador_layout.addWidget(btn_buscar)
        layout.addLayout(buscador_layout)

        # Tabla de asistencias
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Cédula", "Hora Entrada", "Hora Salida", "Fecha Registro"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.cellDoubleClicked.connect(self.abrir_edicion)
        layout.addWidget(self.tabla)

        # Botones exportar Excel y PDF
        botones_layout = QHBoxLayout()
        btn_exportar_excel = QPushButton("Exportar a Excel")
        btn_exportar_excel.clicked.connect(self.exportar_excel)
        btn_exportar_pdf = QPushButton("Exportar a PDF")
        btn_exportar_pdf.clicked.connect(self.exportar_pdf)

        botones_layout.addWidget(btn_exportar_excel)
        botones_layout.addWidget(btn_exportar_pdf)
        layout.addLayout(botones_layout)

        self.setLayout(layout)

        # Carga inicial de datos
        self.cargar_datos()

    def cargar_datos(self, registros=None):
        if registros is None:
            registros = obtener_historial_asistencias()

        self.tabla.setRowCount(len(registros))
        self.registros = registros  # Guardamos para editar luego

        for fila, r in enumerate(registros):
            self.tabla.setItem(fila, 0, QTableWidgetItem(r.get("nombre", "")))
            self.tabla.setItem(fila, 1, QTableWidgetItem(r.get("cedula", "")))
            self.tabla.setItem(fila, 2, QTableWidgetItem(r.get("hora_entrada", "")))
            self.tabla.setItem(fila, 3, QTableWidgetItem(r.get("hora_salida", "")))
            fecha = r.get("fecha_registro", None)
            fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S") if fecha else ""
            self.tabla.setItem(fila, 4, QTableWidgetItem(fecha_str))

    def filtrar_por_cedula(self):
        texto = self.input_busqueda.text().strip()
        registros = obtener_historial_asistencias()
        if texto:
            filtrados = [r for r in registros if texto in r.get("cedula", "")]
            self.cargar_datos(filtrados)
        else:
            self.cargar_datos()

    def abrir_edicion(self, fila, columna):
        if fila < len(self.registros):
            registro = self.registros[fila]
            ventana_edicion = EditarAsistencia(registro)
            if ventana_edicion.exec():
                self.cargar_datos()
                QMessageBox.information(self, "Actualizado", "El registro fue editado con éxito.")

    def exportar_pdf(self):
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "", "PDF Files (*.pdf)")
        if ruta_archivo:
            exito = exportar_asistencias_a_pdf(ruta_archivo)
            if exito:
                QMessageBox.information(self, "Éxito", "PDF exportado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al generar el PDF.")

    def exportar_excel(self):
        from controllers.asistencias_controller import exportar_asistencias_a_excel

        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Excel", "", "Excel Files (*.xlsx)")
        if ruta_archivo:
            exito = exportar_asistencias_a_excel(ruta_archivo)
            if exito:
                QMessageBox.information(self, "Éxito", "Excel exportado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "Hubo un problema al generar el Excel.")
