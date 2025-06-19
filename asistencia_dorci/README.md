# Sistema de Control de Asistencias - DORCI

## 1. Descripción

Esta es una aplicación de escritorio desarrollada en Python y PyQt6 para el manejo y control de asistencias de los empleados de la Dirección de la Oficina Regional de Comunicación e Información (DORCI) de la Gobernación del Estado Falcón.

---

## 2. Características Principales

* **Inicio de Sesión Seguro:** Sistema de autenticación con contraseñas hasheadas.
* **Gestión de Asistencias:** Registro de entradas y salidas, historial completo y capacidad de edición y eliminación.
* **Gestión de Usuarios:** Interfaz para administradores para añadir y eliminar usuarios de la aplicación.
* **Reportes:** Exportación del historial de asistencias a formatos PDF y Excel.
* **Interfaz Moderna:** Diseño de página única con navegación lateral y soporte para temas personalizados.

---

## 3. Cómo Ejecutar la Aplicación

1.  Asegurarse de tener Python 3 instalado.
2.  Instalar las dependencias necesarias:
    ```bash
    pip install PyQt6 pymongo bcrypt openpyxl reportlab qdarkstyle
    ```
3.  Verificar que el servicio de MongoDB esté en ejecución.
4.  Ejecutar el programa desde la terminal, ubicándose en la carpeta raíz del proyecto:
    ```bash
    python main.py
    ```

---

## 4. Estructura del Proyecto

El proyecto está organizado en módulos para separar la lógica de la interfaz y otros componentes.

```
asistencia_dorci/
│
├── assets/
│   └── logo.png          # <-- LOGO OFICIAL de la aplicación. Usado como ícono y en la interfaz.
│
├── controllers/
│   ├── asistencias_controller.py # Lógica para manejar las asistencias.
│   ├── auth_controller.py      # Lógica para la autenticación de usuarios.
│   └── user_controller.py      # Lógica para la gestión de usuarios (CRUD).
│
├── ui/
│   ├── styles.qss              # Hoja de estilos principal de la aplicación.
│   ├── ventana_principal.py    # Ventana principal que contiene la arquitectura.
│   └── ...                     # Demás archivos de la interfaz de usuario.
│
├── database.py             # Módulo central para la conexión con MongoDB.
├── main.py                 # Punto de entrada para ejecutar la aplicación.
├── utils.py                # Funciones de utilidad (ej: formatear cédula).
└── README.md               # Esta documentación.
```

---