# ubicacion: asistencia_dorci/ui/ventana_principal.py

from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QStackedWidget, QLabel, QFrame, QApplication)
# --- NUEVAS IMPORTACIONES PARA ICONOS E IMÁGENES ---
from PyQt6.QtGui import QFont, QIcon, QPixmap
# ----------------------------------------------------
from PyQt6.QtCore import Qt

from .historial_asistencias_page import HistorialAsistenciasPage
from .user_management_page import UserManagementPage
from .formulario_asistencia import FormularioAsistencia

class VentanaPrincipal(QMainWindow):
    def __init__(self, rol_usuario):
        super().__init__()
        self.rol_usuario = rol_usuario
        self.setWindowTitle("Sistema de Control de Asistencias - AsisDORCI")
        self.setMinimumSize(1100, 800)
        self.setObjectName("VentanaPrincipal")

        # --- AÑADIMOS EL ÍCONO A LA VENTANA ---
        self.setWindowIcon(QIcon("assets/logo.png"))
        # ------------------------------------

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Barra de Navegación (Izquierda) ---
        nav_bar = QWidget()
        nav_bar.setObjectName("NavBar")
        nav_bar.setFixedWidth(220)
        nav_layout = QVBoxLayout(nav_bar)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        nav_layout.setContentsMargins(10, 20, 10, 20)
        nav_layout.setSpacing(20)

        # --- MOSTRAMOS EL LOGO EN LUGAR DEL TÍTULO DE TEXTO ---
        logo_label = QLabel()
        pixmap = QPixmap("assets/logo.png")
        # Escalar el pixmap a un tamaño razonable manteniendo la proporción
        scaled_pixmap = pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(logo_label)
        # ---------------------------------------------------

        self.btn_registrar = QPushButton("Registrar Asistencia")
        self.btn_registrar.clicked.connect(self.abrir_formulario_asistencia)
        nav_layout.addWidget(self.btn_registrar)
        
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        nav_layout.addWidget(linea)

        self.btn_historial = QPushButton("Historial de Asistencias")
        self.btn_manage_users = QPushButton("Gestionar Usuarios")
        
        nav_layout.addWidget(self.btn_historial)
        nav_layout.addWidget(self.btn_manage_users)
        
        nav_layout.addStretch()

        self.btn_cerrar_sesion = QPushButton("Cerrar Sesión")
        self.btn_cerrar_sesion.clicked.connect(lambda: QApplication.instance().exit(123))
        nav_layout.addWidget(self.btn_cerrar_sesion)

        if self.rol_usuario != 'admin':
            self.btn_manage_users.hide()

        # ... (El resto del archivo no cambia) ...
        self.stacked_widget = QStackedWidget()
        self.historial_page = HistorialAsistenciasPage()
        self.user_management_page = UserManagementPage()
        self.stacked_widget.addWidget(self.historial_page)
        self.stacked_widget.addWidget(self.user_management_page)
        self.btn_historial.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.historial_page))
        self.btn_manage_users.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.user_management_page))
        main_layout.addWidget(nav_bar)
        main_layout.addWidget(self.stacked_widget, stretch=1)
        self.setCentralWidget(main_widget)
        self.stacked_widget.setCurrentWidget(self.historial_page)

    def abrir_formulario_asistencia(self):
        dialogo = FormularioAsistencia(self)
        if dialogo.exec():
            self.historial_page.cargar_historial()