# ubicacion: asistencia_dorci/database.py

import pymongo
from pymongo.errors import ConnectionFailure
import sys

# --- Configuración Centralizada ---
# Modifica esta URI si tu base de datos está en otro lugar (ej. MongoDB Atlas)
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "DORCI" # Usamos el nombre de la BD que tenías en tus controladores

def get_db():
    """
    Establece la conexión con la base de datos MongoDB y devuelve la instancia de la BD.
    Si la conexión falla, termina la aplicación.
    """
    try:
        cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # El comando 'ping' es una forma ligera de verificar la conexión.
        cliente.admin.command('ping')
        # print("✅ Conexión a MongoDB exitosa.") # Descomentar para depuración
        db = cliente[DB_NAME]
        return db
    except ConnectionFailure:
        print("❌ Error Crítico: No se pudo conectar a MongoDB.", file=sys.stderr)
        print("Verifica que el servidor de MongoDB esté activo y que la URI sea correcta.", file=sys.stderr)
        # En una aplicación de escritorio, si la BD no está, no podemos continuar.
        sys.exit("Aplicación terminada debido a un error de conexión con la base de datos.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado al conectar a la BD: {e}", file=sys.stderr)
        sys.exit("Aplicación terminada debido a un error inesperado.")

# --- Instancia Única de la Base de Datos ---
# Esta es la variable que importarán todos los demás módulos.
# La conexión se establece una sola vez cuando la aplicación arranca.
db = get_db()