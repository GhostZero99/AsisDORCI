# ui/formulario_asistencia.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import QDateTime
from controllers.asistencias_controller import guardar_asistencia

class FormularioAsistencia(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Asistencia")
        self.setMinimumWidth(400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nombre_input = QLineEdit()
        self.cedula_input = QLineEdit()
        self.hora_entrada_input = QLineEdit()
        self.hora_salida_input = QLineEdit()

        self.hora_entrada_input.setText(QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"))
        self.hora_entrada_input.setReadOnly(True)

        layout.addLayout(self.crear_fila("Nombre completo:", self.nombre_input))
        layout.addLayout(self.crear_fila("Cédula:", self.cedula_input))
        layout.addLayout(self.crear_fila("Hora de entrada:", self.hora_entrada_input))
        layout.addLayout(self.crear_fila("Hora de salida (opcional):", self.hora_salida_input))

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar)

        layout.addWidget(btn_guardar)
        self.setLayout(layout)

    def crear_fila(self, etiqueta, campo):
        fila = QHBoxLayout()
        fila.addWidget(QLabel(etiqueta))
        fila.addWidget(campo)
        return fila

    def guardar(self):
        nombre = self.nombre_input.text().strip()
        cedula = self.cedula_input.text().strip()
        hora_entrada = self.hora_entrada_input.text().strip()
        hora_salida = self.hora_salida_input.text().strip()

        if not nombre or not cedula:
            QMessageBox.warning(self, "Campos requeridos", "Nombre y Cédula son obligatorios.")
            return

        asistencia = {
            "nombre": nombre,
            "cedula": cedula,
            "hora_entrada": hora_entrada,
            "hora_salida": hora_salida if hora_salida else None
        }

        exito = guardar_asistencia(asistencia)
        if exito:
            QMessageBox.information(self, "Éxito", "Asistencia registrada correctamente.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la asistencia.")
