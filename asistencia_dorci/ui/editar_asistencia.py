# ubicacion: asistencia_dorci/ui/editar_asistencia.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from controllers.asistencias_controller import actualizar_asistencia

class EditarAsistenciaDialog(QDialog):
    def __init__(self, asistencia, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Registro de Asistencia")
        self.asistencia = asistencia
        # --- TAMAÑO ACTUALIZADO ---
        self.setFixedSize(400, 420) # Aumentamos la altura para más espacio
        # --------------------------

        layout = QVBoxLayout(self)

        # Campos del formulario
        self.nombre_input = QLineEdit(self.asistencia.get("nombre_completo"))
        self.cedula_input = QLineEdit(self.asistencia.get("cedula"))
        # Hacemos que la cédula no se pueda editar para mantener la integridad del registro
        self.cedula_input.setReadOnly(True)
        
        self.fecha_input = QLineEdit(self.asistencia.get("fecha"))
        self.hora_entrada_input = QLineEdit(self.asistencia.get("hora_entrada"))
        self.hora_salida_input = QLineEdit(self.asistencia.get("hora_salida", ""))

        layout.addWidget(QLabel("Nombre Completo:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("Cédula de Identidad (No editable):"))
        layout.addWidget(self.cedula_input)
        layout.addWidget(QLabel("Fecha:"))
        layout.addWidget(self.fecha_input)
        layout.addWidget(QLabel("Hora de Entrada:"))
        layout.addWidget(self.hora_entrada_input)
        layout.addWidget(QLabel("Hora de Salida:"))
        layout.addWidget(self.hora_salida_input)

        # Botón de guardar
        self.guardar_button = QPushButton("Guardar Cambios")
        self.guardar_button.clicked.connect(self.guardar_cambios)
        layout.addWidget(self.guardar_button)

    def guardar_cambios(self):
        # Creamos un diccionario solo con los campos que se pueden modificar
        nuevos_datos = {
            "nombre_completo": self.nombre_input.text(),
            "fecha": self.fecha_input.text(),
            "hora_entrada": self.hora_entrada_input.text(),
            "hora_salida": self.hora_salida_input.text()
        }

        # Una validación simple para los campos editables
        if not all([nuevos_datos["nombre_completo"], nuevos_datos["fecha"], nuevos_datos["hora_entrada"]]):
            QMessageBox.warning(self, "Datos incompletos", "Nombre, fecha y hora de entrada son obligatorios.")
            return

        asistencia_id = self.asistencia.get("_id")
        if actualizar_asistencia(asistencia_id, nuevos_datos):
            QMessageBox.information(self, "Éxito", "La asistencia ha sido actualizada.")
            self.accept()  # Cierra el diálogo si la actualización fue exitosa
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar la asistencia.")