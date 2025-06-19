# ubicacion: asistencia_dorci/controllers/user_controller.py

import bcrypt
from bson.objectid import ObjectId
from database import db

def get_all_users():
    """
    Obtiene todos los usuarios de la base de datos, excluyendo sus contraseñas.
    """
    try:
        usuarios_collection = db['usuarios']
        # El segundo argumento {'password': 0} excluye el campo de la contraseña de los resultados
        return list(usuarios_collection.find({}, {'password': 0}))
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def create_user(username, password, rol):
    """
    Crea un nuevo usuario con la contraseña hasheada.
    Retorna (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    try:
        usuarios_collection = db['usuarios']
        if usuarios_collection.find_one({'username': username}):
            return False, f"El usuario '{username}' ya existe."

        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        usuarios_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'rol': rol
        })
        return True, f"Usuario '{username}' creado exitosamente."
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False, "Ocurrió un error en la base de datos."

def delete_user(user_id):
    """
    Elimina un usuario por su ID.
    Previene la eliminación del último administrador.
    """
    try:
        usuarios_collection = db['usuarios']
        
        # Comprobación para no eliminar al último admin
        user_to_delete = usuarios_collection.find_one({'_id': ObjectId(user_id)})
        if user_to_delete and user_to_delete.get('rol') == 'admin':
            admin_count = usuarios_collection.count_documents({'rol': 'admin'})
            if admin_count <= 1:
                return False, "No se puede eliminar al único administrador del sistema."

        # Si pasa la validación, se elimina
        result = usuarios_collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count > 0:
            return True, "Usuario eliminado correctamente."
        else:
            return False, "No se encontró al usuario para eliminar."
            
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False, "Ocurrió un error en la base de datos."