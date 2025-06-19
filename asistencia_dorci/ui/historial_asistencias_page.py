# ubicacion: asistencia_dorci/ui/historial_asistencias_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QHBoxLayout, QFileDialog, QMessageBox,
                             QFormLayout, QLineEdit, QDateEdit, QLabel, QFrame, QHeaderView)
from PyQt6.QtCore import Qt, QDate
from controllers.asistencias_controller import obtener_asistencias, exportar_a_pdf, exportar_a_excel, eliminar_asistencia
from utils import format_cedula
# --- RE-ACTIVAMOS LA IMPORTACIÓN DEL DIÁLOGO DE EDICIÓN ---
from .editar_asistencia import EditarAsistenciaDialog

class HistorialAsistenciasPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        # --- Formulario de Filtros (sin cambios) ---
        filter_group = QFrame()
        filter_group.setObjectName("FilterGroup")
        form_layout = QFormLayout(filter_group)
        # ... (todo el código del formulario de filtros se queda igual) ...
        form_layout.setContentsMargins(10, 10, 10, 10)
        self.cedula_filter_input = QLineEdit()
        self.cedula_filter_input.setPlaceholderText("Buscar por Cédula (sin puntos)")
        self.cedula_filter_input.returnPressed.connect(self.aplicar_filtros)
        form_layout.addRow(QLabel("Filtrar por Empleado:"), self.cedula_filter_input)
        self.fecha_inicio_input = QDateEdit(calendarPopup=True)
        self.fecha_inicio_input.setDisplayFormat("dd-MM-yyyy")
        self.fecha_inicio_input.setDate(QDate.currentDate().addMonths(-1))
        form_layout.addRow(QLabel("Fecha de Inicio:"), self.fecha_inicio_input)
        self.fecha_fin_input = QDateEdit(calendarPopup=True)
        self.fecha_fin_input.setDisplayFormat("dd-MM-yyyy")
        self.fecha_fin_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Fecha de Fin:"), self.fecha_fin_input)
        filter_button_layout = QHBoxLayout()
        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.clicked.connect(self.aplicar_filtros)
        self.btn_limpiar = QPushButton("Limpiar Filtros")
        self.btn_limpiar.clicked.connect(self.limpiar_filtros)
        filter_button_layout.addWidget(self.btn_filtrar)
        filter_button_layout.addWidget(self.btn_limpiar)
        form_layout.addRow(filter_button_layout)
        layout.addWidget(filter_group)
        
        # --- Tabla de Asistencias (sin cambios) ---
        self.tabla_asistencias = QTableWidget()
        # ... (todo el código de configuración de la tabla se queda igual) ...
        self.tabla_asistencias.setColumnCount(6)
        self.tabla_asistencias.setHorizontalHeaderLabels(["ID", "Nombre Completo", "Cédula", "Fecha", "Hora de Entrada", "Hora de Salida"])
        self.tabla_asistencias.setColumnHidden(0, True)
        self.tabla_asistencias.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_asistencias.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.tabla_asistencias.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.tabla_asistencias)

        # --- Botones de Acción (con el nuevo botón de Editar) ---
        bottom_button_layout = QHBoxLayout()
        self.btn_exportar_excel = QPushButton("Exportar a Excel")
        self.btn_exportar_excel.clicked.connect(self.manejador_exportar_excel)
        bottom_button_layout.addWidget(self.btn_exportar_excel)
        
        self.btn_exportar_pdf = QPushButton("Exportar a PDF")
        self.btn_exportar_pdf.clicked.connect(self.manejador_exportar_pdf)
        bottom_button_layout.addWidget(self.btn_exportar_pdf)

        # --- NUEVO BOTÓN PARA EDITAR ---
        self.btn_editar = QPushButton("Editar")
        self.btn_editar.setEnabled(False) # Deshabilitado por defecto
        self.btn_editar.clicked.connect(self.editar_asistencia_seleccionada)
        bottom_button_layout.addWidget(self.btn_editar)
        
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setEnabled(False)
        self.btn_eliminar.clicked.connect(self.eliminar_asistencia_seleccionada)
        bottom_button_layout.addWidget(self.btn_eliminar)
        
        layout.addLayout(bottom_button_layout)
        self.setLayout(layout)

        # Conectar la selección de la tabla a la activación de los botones
        self.tabla_asistencias.itemSelectionChanged.connect(self.actualizar_estado_botones_accion)

        self.cargar_historial()

    # --- FUNCIÓN DE ESTADO DE BOTONES ACTUALIZADA ---
    def actualizar_estado_botones_accion(self):
        # Habilita los botones de acción solo si hay una fila seleccionada
        hay_seleccion = len(self.tabla_asistencias.selectedItems()) > 0
        self.btn_editar.setEnabled(hay_seleccion)
        self.btn_eliminar.setEnabled(hay_seleccion)

    # --- NUEVA FUNCIÓN PARA EDITAR REGISTRO ---
    def editar_asistencia_seleccionada(self):
        selected_rows = self.tabla_asistencias.selectionModel().selectedRows()
        if not selected_rows:
            return

        # Buscamos el diccionario completo del registro seleccionado en nuestra lista de datos
        selected_id = self.tabla_asistencias.item(selected_rows[0].row(), 0).text()
        registro_a_editar = None
        for registro in self.asistencias:
            if str(registro['_id']) == selected_id:
                registro_a_editar = registro
                break
        
        if registro_a_editar:
            # Abrimos el diálogo de edición, pasándole los datos del registro
            dialogo = EditarAsistenciaDialog(registro_a_editar, self)
            # Si el diálogo se cierra con "Aceptar" (es decir, se guardaron cambios)...
            if dialogo.exec():
                self.cargar_historial() # Recargamos la tabla para ver los cambios

    # --- El resto de funciones permanecen igual ---
    def eliminar_asistencia_seleccionada(self):
        selected_rows = self.tabla_asistencias.selectionModel().selectedRows()
        if not selected_rows:
            return
        asistencia_id = self.tabla_asistencias.item(selected_rows[0].row(), 0).text()
        nombre = self.tabla_asistencias.item(selected_rows[0].row(), 1).text()
        fecha = self.tabla_asistencias.item(selected_rows[0].row(), 3).text()
        reply = QMessageBox.question(self, "Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar el registro de:\n\n{nombre} del día {fecha}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if eliminar_asistencia(asistencia_id):
                QMessageBox.information(self, "Éxito", "El registro de asistencia ha sido eliminado.")
                self.cargar_historial()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el registro.")

    def cargar_historial(self, filtros=None):
        self.asistencias = obtener_asistencias(filtros)
        self.tabla_asistencias.setRowCount(len(self.asistencias))
        for row, item in enumerate(self.asistencias):
            item_id = str(item.get('_id', ''))
            cedula_sin_formato = item.get("cedula", "")
            cedula_con_formato = format_cedula(cedula_sin_formato)
            self.tabla_asistencias.setItem(row, 0, QTableWidgetItem(item_id))
            self.tabla_asistencias.setItem(row, 1, QTableWidgetItem(item.get("nombre_completo", "")))
            self.tabla_asistencias.setItem(row, 2, QTableWidgetItem(cedula_con_formato))
            self.tabla_asistencias.setItem(row, 3, QTableWidgetItem(item.get("fecha", "")))
            self.tabla_asistencias.setItem(row, 4, QTableWidgetItem(item.get("hora_entrada", "")))
            self.tabla_asistencias.setItem(row, 5, QTableWidgetItem(item.get("hora_salida", "")))

    def aplicar_filtros(self):
        cedula_a_filtrar = self.cedula_filter_input.text().replace('.', '')
        filtros = {"cedula": cedula_a_filtrar, "fecha_inicio": self.fecha_inicio_input.date().toString("dd-MM-yyyy"), "fecha_fin": self.fecha_fin_input.date().toString("dd-MM-yyyy")}
        self.cargar_historial(filtros)

    def limpiar_filtros(self):
        self.cedula_filter_input.clear()
        self.fecha_inicio_input.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_fin_input.setDate(QDate.currentDate())
        self.cargar_historial()

    def manejador_exportar_excel(self):
        if not hasattr(self, 'asistencias') or not self.asistencias:
            QMessageBox.warning(self, "Datos Vacíos", "No hay datos para exportar.")
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar como Excel", "", "Excel Files (*.xlsx)")
        if filepath:
            if exportar_a_excel(self.asistencias, filepath):
                QMessageBox.information(self, "Éxito", "Historial exportado a Excel correctamente.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo exportar el historial a Excel.")

    def manejador_exportar_pdf(self):
        if not hasattr(self, 'asistencias') or not self.asistencias:
            QMessageBox.warning(self, "Datos Vacíos", "No hay datos para exportar.")
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar como PDF", "", "PDF Files (*.pdf)")
        if filepath:
            if exportar_a_pdf(self.asistencias, filepath):
                QMessageBox.information(self, "Éxito", "Historial exportado a PDF correctamente.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo exportar el historial a PDF.")