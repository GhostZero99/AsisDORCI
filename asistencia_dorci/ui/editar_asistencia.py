# ui/editar_asistencia.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from controllers.asistencias_controller import actualizar_asistencia

class EditarAsistencia(QDialog):
    def __init__(self, registro):
        super().__init__()
        self.registro = registro
        self.setWindowTitle("Editar Asistencia")
        self.resize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_nombre = QLineEdit(self.registro.get("nombre", ""))
        self.input_cedula = QLineEdit(self.registro.get("cedula", ""))
        self.input_entrada = QLineEdit(self.registro.get("hora_entrada", ""))
        self.input_salida = QLineEdit(self.registro.get("hora_salida", ""))

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.input_nombre)
        layout.addWidget(QLabel("Cédula:"))
        layout.addWidget(self.input_cedula)
        layout.addWidget(QLabel("Hora de Entrada:"))
        layout.addWidget(self.input_entrada)
        layout.addWidget(QLabel("Hora de Salida:"))
        layout.addWidget(self.input_salida)

        btn_guardar = QPushButton("Guardar Cambios")
        btn_guardar.clicked.connect(self.guardar)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)

    def guardar(self):
        datos = {
            "nombre": self.input_nombre.text().strip(),
            "cedula": self.input_cedula.text().strip(),
            "hora_entrada": self.input_entrada.text().strip(),
            "hora_salida": self.input_salida.text().strip()
        }

        exito = actualizar_asistencia(self.registro["_id"], datos)
        if exito:
            QMessageBox.information(self, "Éxito", "Registro actualizado correctamente.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar el registro.")
