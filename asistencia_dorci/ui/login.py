# ubicacion: asistencia_dorci/ui/login.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QCheckBox
from controllers.auth_controller import verificar_credenciales
from utils import guardar_ultimo_usuario, cargar_ultimo_usuario

class LoginVentana(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión - Sistema de Asistencias DORCI")
        self.setFixedSize(350, 230)

        self.user_rol = None
        self.username = None

        layout = QVBoxLayout()

        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Nombre de usuario")
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.usuario_input)

        self.contrasena_input = QLineEdit()
        self.contrasena_input.setPlaceholderText("Contraseña")
        self.contrasena_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.contrasena_input)

        self.check_recordar = QCheckBox("Recordar usuario")
        layout.addWidget(self.check_recordar)

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.intentar_login)
        layout.addWidget(self.login_button)

        self.login_button.setDefault(True)
        self.contrasena_input.returnPressed.connect(self.login_button.click)

        self.setLayout(layout)
        
        self.precargar_usuario()

    def precargar_usuario(self):
        """Revisa si hay un usuario guardado y lo pone en el campo de texto."""
        ultimo_usuario = cargar_ultimo_usuario()
        if ultimo_usuario:
            self.usuario_input.setText(ultimo_usuario)
            self.check_recordar.setChecked(True)
            self.contrasena_input.setFocus()

    def intentar_login(self):
        username = self.usuario_input.text()
        password = self.contrasena_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Datos incompletos", "Por favor, ingrese usuario y contraseña.")
            return

        es_valido, rol = verificar_credenciales(username, password)
        
        if es_valido:
            if self.check_recordar.isChecked():
                guardar_ultimo_usuario(username)
            else:
                guardar_ultimo_usuario(None) # Pasamos None para que se borre del config

            self.username = username
            self.user_rol = rol
            self.accept()
        else:
            QMessageBox.critical(self, "Error de autenticación", "Usuario o contraseña incorrectos.")
            self.contrasena_input.clear()