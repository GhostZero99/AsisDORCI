# controllers/auth_controller.py

from pymongo import MongoClient

def obtener_conexion():
    cliente = MongoClient("mongodb://localhost:27017/")
    return cliente["control_asistencias_dorci"]

def validar_usuario(username, password):
    db = obtener_conexion()
    usuario = db.usuarios.find_one({"username": username, "password": password})
    if usuario:
        return usuario.get("rol", "usuario")
    return None
