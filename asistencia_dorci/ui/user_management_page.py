# ubicacion: asistencia_dorci/ui/user_management_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, QInputDialog,
                             QComboBox, QLineEdit, QHeaderView) # <-- Importamos QHeaderView
from PyQt6.QtCore import Qt
from controllers.user_controller import get_all_users, create_user, delete_user

class UserManagementPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        self.table_users = QTableWidget()
        self.table_users.setColumnCount(3)
        self.table_users.setHorizontalHeaderLabels(["ID", "Nombre de Usuario", "Rol"])
        self.table_users.setColumnHidden(0, True)
        self.table_users.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_users.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # --- NUEVA SECCIÓN PARA LA RESPONSIVIDAD ---
        header = self.table_users.horizontalHeader()
        # La columna "Nombre de Usuario" (índice 1) se estirará
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # La columna "Rol" se ajustará a su contenido
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        # ----------------------------------------
        
        layout.addWidget(self.table_users)

        button_layout = QHBoxLayout()
        self.btn_add = QPushButton("Añadir Usuario")
        self.btn_add.clicked.connect(self.add_new_user)
        button_layout.addWidget(self.btn_add)
        self.btn_delete = QPushButton("Eliminar Usuario")
        self.btn_delete.clicked.connect(self.delete_selected_user)
        button_layout.addWidget(self.btn_delete)
        layout.addLayout(button_layout)

        self.load_users_data()

    def load_users_data(self):
        self.table_users.setRowCount(0)
        users = get_all_users()
        for row, user in enumerate(users):
            self.table_users.insertRow(row)
            self.table_users.setItem(row, 0, QTableWidgetItem(str(user['_id'])))
            self.table_users.setItem(row, 1, QTableWidgetItem(user['username']))
            self.table_users.setItem(row, 2, QTableWidgetItem(user['rol']))
        # Ya no necesitamos esto: self.table_users.resizeColumnsToContents()
    
    # ... (El resto de las funciones (add_new_user, etc.) son iguales) ...
    def add_new_user(self):
        username, ok1 = QInputDialog.getText(self, "Nuevo Usuario", "Nombre de usuario:")
        if ok1 and username:
            password, ok2 = QInputDialog.getText(self, "Nuevo Usuario", f"Contraseña para {username}:", QLineEdit.EchoMode.Password)
            if ok2 and password:
                roles = ["empleado", "admin"]
                rol, ok3 = QInputDialog.getItem(self, "Nuevo Usuario", "Rol:", roles, 0, False)
                if ok3 and rol:
                    success, message = create_user(username, password, rol)
                    QMessageBox.information(self, "Crear Usuario", message)
                    if success:
                        self.load_users_data()
    def delete_selected_user(self):
        selected_rows = self.table_users.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selección Requerida", "Por favor, selecciona un usuario de la lista para eliminar.")
            return
        selected_row = selected_rows[0].row()
        user_id = self.table_users.item(selected_row, 0).text()
        username = self.table_users.item(selected_row, 1).text()
        reply = QMessageBox.question(self, "Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar al usuario '{username}'?\n¡Esta acción no se puede deshacer!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            success, message = delete_user(user_id)
            QMessageBox.information(self, "Eliminar Usuario", message)
            if success:
                self.load_users_data()