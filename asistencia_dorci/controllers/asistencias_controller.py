# ubicacion: asistencia_dorci/controllers/asistencias_controller.py

from database import db
from bson.objectid import ObjectId
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def guardar_asistencia(data):
    try:
        asistencias_collection = db['asistencias']
        asistencias_collection.insert_one(data)
        return True
    except Exception as e:
        print(f"Error al guardar asistencia: {e}")
        return False

# --- FUNCIÓN MODIFICADA ---
def obtener_asistencias(filtros=None):
    """
    Obtiene los registros de asistencia, aplicando filtros si se proporcionan.
    'filtros' es un diccionario que puede contener 'cedula', 'fecha_inicio', 'fecha_fin'.
    """
    try:
        asistencias_collection = db['asistencias']
        query = {}
        
        if filtros:
            if filtros.get("cedula"):
                query["cedula"] = {"$regex": filtros["cedula"], "$options": "i"} # Búsqueda flexible

            if filtros.get("fecha_inicio") and filtros.get("fecha_fin"):
                query["fecha"] = {
                    "$gte": filtros["fecha_inicio"],
                    "$lte": filtros["fecha_fin"]
                }
        
        # Ordenamos los resultados por fecha descendente para ver los más recientes primero
        return list(asistencias_collection.find(query).sort("fecha", -1))
    except Exception as e:
        print(f"Error al obtener asistencias: {e}")
        return []

def actualizar_asistencia(asistencia_id, nuevos_datos):
    try:
        asistencias_collection = db['asistencias']
        obj_id = ObjectId(asistencia_id)
        resultado = asistencias_collection.update_one({'_id': obj_id}, {'$set': nuevos_datos})
        return resultado.modified_count > 0
    except Exception as e:
        print(f"Error al actualizar asistencia: {e}")
        return False

def eliminar_asistencia(asistencia_id):
    try:
        asistencias_collection = db['asistencias']
        obj_id = ObjectId(asistencia_id)
        resultado = asistencias_collection.delete_one({'_id': obj_id})
        return resultado.deleted_count > 0
    except Exception as e:
        print(f"Error al eliminar asistencia: {e}")
        return False

def exportar_a_excel(asistencias, filepath):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Historial de Asistencias"
        headers = ["Nombre Completo", "Cédula", "Fecha", "Hora de Entrada", "Hora de Salida"]
        ws.append(headers)
        for item in asistencias:
            ws.append([
                item.get("nombre_completo", ""),
                item.get("cedula", ""),
                item.get("fecha", ""),
                item.get("hora_entrada", ""),
                item.get("hora_salida", "")
            ])
        wb.save(filepath)
        return True
    except Exception as e:
        print(f"Error al exportar a Excel: {e}")
        return False

def exportar_a_pdf(asistencias, filepath):
    try:
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Historial de Asistencias - DORCI", styles['h1']))
        data = [["Nombre Completo", "Cédula", "Fecha", "H. Entrada", "H. Salida"]]
        for item in asistencias:
            data.append([
                item.get("nombre_completo", ""),
                item.get("cedula", ""),
                item.get("fecha", ""),
                item.get("hora_entrada", ""),
                item.get("hora_salida", "")
            ])
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        elements.append(table)
        doc.build(elements)
        return True
    except Exception as e:
        print(f"Error al exportar a PDF: {e}")
        return False