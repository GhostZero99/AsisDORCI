# ubicacion: asistencia_dorci/utils.py

import json

CONFIG_FILE = "config.json"

def format_cedula(cedula_str):
    """
    Toma un string de números y le da formato de cédula con puntos.
    """
    if not cedula_str or "." in cedula_str:
        return cedula_str
    try:
        formatted_cedula = f"{int(cedula_str):_}".replace("_", ".")
        return formatted_cedula
    except (ValueError, TypeError):
        return cedula_str

def guardar_ultimo_usuario(username):
    """Guarda el nombre de usuario en el archivo de configuración."""
    try:
        # Si el username es None o vacío, guardamos un string vacío.
        user_to_save = username if username else ""
        with open(CONFIG_FILE, "w") as f:
            json.dump({"ultimo_usuario": user_to_save}, f)
    except Exception as e:
        print(f"Error al guardar configuración: {e}")

def cargar_ultimo_usuario():
    """Carga el nombre del último usuario desde el archivo de configuración."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("ultimo_usuario")
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
        return None