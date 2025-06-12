# controllers/asistencias_controller.py

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import os
from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def obtener_conexion():
    try:
        cliente = MongoClient("mongodb://localhost:27017/")
        db = cliente["control_asistencias_dorci"]
        return db
    except Exception as e:
        print("Error de conexión:", e)
        return None

def guardar_asistencia(nombre, cedula, hora_entrada, hora_salida):
    db = obtener_conexion()
    if db:
        asistencia = {
            "nombre": nombre,
            "cedula": cedula,
            "hora_entrada": hora_entrada,
            "hora_salida": hora_salida,
            "fecha_registro": datetime.now()
        }
        try:
            db.asistencias.insert_one(asistencia)
            return True
        except Exception as e:
            print("Error al guardar asistencia:", e)
            return False
    return False

def obtener_historial_asistencias():
    db = obtener_conexion()
    if db:
        try:
            return list(db.asistencias.find().sort("fecha_registro", -1))
        except Exception as e:
            print("Error al obtener historial:", e)
            return []
    return []

def exportar_asistencias_a_excel(ruta_archivo):
    asistencias = obtener_historial_asistencias()
    wb = Workbook()
    ws = wb.active
    ws.title = "Historial Asistencias"

    headers = ["Nombre", "Cédula", "Hora Entrada", "Hora Salida", "Fecha Registro"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for r in asistencias:
        ws.append([
            r.get("nombre", ""),
            r.get("cedula", ""),
            r.get("hora_entrada", ""),
            r.get("hora_salida", ""),
            r.get("fecha_registro", "").strftime("%Y-%m-%d %H:%M:%S") if r.get("fecha_registro") else ""
        ])

    try:
        wb.save(ruta_archivo)
        return True
    except Exception as e:
        print("Error al exportar Excel:", e)
        return False

def actualizar_asistencia(registro_id, datos_actualizados):
    db = obtener_conexion()
    if db:
        try:
            db.asistencias.update_one(
                {"_id": ObjectId(registro_id)},
                {"$set": datos_actualizados}
            )
            return True
        except Exception as e:
            print("Error al actualizar asistencia:", e)
            return False
    return False

def exportar_asistencias_a_pdf(ruta_archivo):
    registros = obtener_historial_asistencias()
    try:
        c = canvas.Canvas(ruta_archivo, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, height - 40, "Reporte de Asistencias - DORCI")

        c.setFont("Helvetica", 10)
        y = height - 70
        c.drawString(40, y, "Nombre")
        c.drawString(160, y, "Cédula")
        c.drawString(260, y, "Entrada")
        c.drawString(340, y, "Salida")
        c.drawString(420, y, "Fecha Registro")

        y -= 20
        for r in registros:
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(40, y, (r.get("nombre", "") or "")[:18])
            c.drawString(160, y, r.get("cedula", ""))
            c.drawString(260, y, r.get("hora_entrada", ""))
            c.drawString(340, y, r.get("hora_salida", ""))
            fecha = r.get("fecha_registro")
            fecha_str = fecha.strftime("%Y-%m-%d %H:%M") if fecha else ""
            c.drawString(420, y, fecha_str)
            y -= 20

        c.save()
        return True
    except Exception as e:
        print("Error al generar PDF:", e)
        return False
