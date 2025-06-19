# ubicacion: asistencia_dorci/ui/formulario_asistencia.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout
from PyQt6.QtCore import QDate, QTime, Qt, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from controllers.asistencias_controller import guardar_asistencia

class FormularioAsistencia(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Asistencia")
        # --- TAMAÑO ACTUALIZADO ---
        self.setFixedSize(400, 400) # Aumentamos la altura para dar más espacio
        # --------------------------

        layout = QVBoxLayout(self)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ingrese nombre completo")
        nombre_regex = QRegularExpression("[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+")
        nombre_validator = QRegularExpressionValidator(nombre_regex, self)
        self.nombre_input.setValidator(nombre_validator)
        layout.addWidget(QLabel("Nombre Completo:"))
        layout.addWidget(self.nombre_input)

        self.cedula_input = QLineEdit()
        self.cedula_input.setPlaceholderText("Ej: 12.345.678")
        cedula_regex = QRegularExpression("[\d\.]+")
        cedula_validator = QRegularExpressionValidator(cedula_regex, self)
        self.cedula_input.setValidator(cedula_validator)
        layout.addWidget(QLabel("Cédula de Identidad:"))
        layout.addWidget(self.cedula_input)

        self.fecha_input = QLineEdit()
        self.fecha_input.setReadOnly(True)
        self.fecha_input.setText(QDate.currentDate().toString("dd-MM-yyyy"))
        layout.addWidget(QLabel("Fecha:"))
        layout.addWidget(self.fecha_input)
        
        self.hora_entrada_input = QLineEdit()
        self.hora_entrada_input.setReadOnly(True)
        self.hora_entrada_input.setText(QTime.currentTime().toString("hh:mm:ss"))
        layout.addWidget(QLabel("Hora de Entrada:"))
        layout.addWidget(self.hora_entrada_input)

        self.guardar_button = QPushButton("Guardar Asistencia")
        self.guardar_button.clicked.connect(self.guardar)
        
        self.nombre_input.returnPressed.connect(self.guardar_button.click)
        self.cedula_input.returnPressed.connect(self.guardar_button.click)

        layout.addWidget(self.guardar_button)

    def guardar(self):
        cedula_limpia = self.cedula_input.text().replace('.', '')
        data = {
            "nombre_completo": self.nombre_input.text().strip(),
            "cedula": cedula_limpia,
            "fecha": self.fecha_input.text(),
            "hora_entrada": self.hora_entrada_input.text(),
            "hora_salida": ""
        }

        if not data["nombre_completo"] or not data["cedula"]:
            QMessageBox.warning(self, "Datos Incompletos", "El nombre y la cédula son obligatorios.")
            return

        if guardar_asistencia(data):
            QMessageBox.information(self, "Éxito", "Asistencia registrada correctamente.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la asistencia.")