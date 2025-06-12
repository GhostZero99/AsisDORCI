# scripts/crear_usuarios.py (solo para preparar DB)
from pymongo import MongoClient

def crear_usuarios():
    cliente = MongoClient("mongodb://localhost:27017/")
    db = cliente["control_asistencias_dorci"]
    usuarios = db.usuarios

    usuarios.delete_many({})  # Limpiar colección

    usuarios.insert_many([
        {"username": "admin", "password": "admin123", "rol": "admin"},
        {"username": "usuario1", "password": "user123", "rol": "usuario"},
    ])

if __name__ == "__main__":
    crear_usuarios()
    print("Usuarios creados.")

# ui/login.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from controllers.auth_controller import validar_usuario

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Sistema de Asistencias DORCI")
        self.setGeometry(300, 300, 350, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        lbl_usuario = QLabel("Usuario:")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su usuario")

        lbl_password = QLabel("Contraseña:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Ingresar")
        self.btn_login.clicked.connect(self.intentar_login)

        layout.addWidget(lbl_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(lbl_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def intentar_login(self):
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()

        if not usuario or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return

        rol = validar_usuario(usuario, password)
        if rol:
            QMessageBox.information(self, "Bienvenido", f"Login exitoso como {rol}")
            # Emitir señal o llamar ventana principal con rol
            self.rol_usuario = rol
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos")
