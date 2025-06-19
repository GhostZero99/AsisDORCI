# ubicacion: asistencia_dorci/scripts/crear_usuarios.py

import bcrypt
from database import db # La importación ahora funcionará por el modo de ejecución

def crear_admin_si_no_existe():
    """
    Verifica si existe un usuario con el rol 'admin'.
    Si no existe, crea uno con credenciales por defecto y contraseña hasheada.
    """
    try:
        usuarios_collection = db['usuarios']
        admin_existente = usuarios_collection.find_one({'rol': 'admin'})

        if admin_existente:
            print("✅ Un usuario administrador ya existe en la base de datos.")
            return

        print("No se encontró un usuario administrador. Creando uno nuevo...")
        
        admin_user = "admin"
        admin_pass = "admin123"

        password_bytes = admin_pass.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        usuarios_collection.insert_one({
            'username': admin_user,
            'password': hashed_password,
            'rol': 'admin'
        })
        print("==========================================================")
        print("🎉 Usuario Administrador Creado Exitosamente 🎉")
        print(f"   Usuario: {admin_user}")
        print(f"   Contraseña: {admin_pass}")
        print("¡Recuerda cambiar esta contraseña desde la aplicación!")
        print("==========================================================")

    except Exception as e:
        print(f"❌ Error al intentar crear el usuario administrador: {e}")

if __name__ == "__main__":
    crear_admin_si_no_existe()