# controllers/asistencias_controller.py

from pymongo import MongoClient
import datetime
import pandas as pd

def obtener_conexion():
    cliente = MongoClient("mongodb://localhost:27017/")
    return cliente["control_asistencias_dorci"]

def registrar_asistencia(nombre, cedula, hora_llegada, hora_salida):
    db = obtener_conexion()
    asistencias = db.asistencias
    asistencia = {
        "nombre": nombre,
        "cedula": cedula,
        "hora_llegada": hora_llegada,
        "hora_salida": hora_salida,
        "fecha_registro": datetime.datetime.now()
    }
    result = asistencias.insert_one(asistencia)
    return result.inserted_id

def obtener_todas_asistencias():
    db = obtener_conexion()
    asistencias = db.asistencias
    registros = list(asistencias.find().sort("fecha_registro", -1))
    return registros

def exportar_asistencias_a_excel(ruta_archivo):
    registros = obtener_todas_asistencias()
    if not registros:
        return False

    # Convertir documentos Mongo a DataFrame, ignorando _id ObjectId (convertir a str)
    datos = []
    for r in registros:
        datos.append({
            "Nombre": r.get("nombre", ""),
            "Cédula": r.get("cedula", ""),
            "Hora de Llegada": r.get("hora_llegada", ""),
            "Hora de Salida": r.get("hora_salida", ""),
            "Fecha Registro": r.get("fecha_registro", "").strftime("%Y-%m-%d %H:%M:%S") if r.get("fecha_registro") else ""
        })

    df = pd.DataFrame(datos)
    df.to_excel(ruta_archivo, index=False)
    return True
