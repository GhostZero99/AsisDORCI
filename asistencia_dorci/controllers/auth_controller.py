# ubicacion: asistencia_dorci/controllers/auth_controller.py

import bcrypt  # Importamos la librería para hashear
from database import db

def verificar_credenciales(username, password):
    """
    Verifica las credenciales del usuario comparando la contraseña ingresada
    con el hash almacenado en la base de datos.
    """
    try:
        usuarios_collection = db['usuarios']
        usuario = usuarios_collection.find_one({'username': username})

        # Si el usuario existe y la contraseña es correcta
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario['password']):
            # Devolvemos el rol para usarlo más adelante en la aplicación
            return True, usuario.get('rol', 'empleado')
        else:
            # Usuario no encontrado o contraseña incorrecta
            return False, None
    except Exception as e:
        print(f"Error al verificar credenciales: {e}")
        return False, None

def crear_usuario(username, password, rol='empleado'):
    """
    Crea un nuevo usuario en la colección de usuarios con una contraseña hasheada.
    """
    try:
        usuarios_collection = db['usuarios']
        # Comprobar si el usuario ya existe
        if usuarios_collection.find_one({'username': username}):
            print(f"El usuario '{username}' ya existe.")
            return False

        # --- Proceso de Hashing de la contraseña ---
        # 1. Convertimos la contraseña a bytes
        password_bytes = password.encode('utf-8')
        # 2. Generamos una "sal" (salt) para asegurar el hash
        salt = bcrypt.gensalt()
        # 3. Creamos el hash seguro
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        nuevo_usuario = {
            'username': username,
            'password': hashed_password,  # Guardamos el hash, no la contraseña original
            'rol': rol
        }
        usuarios_collection.insert_one(nuevo_usuario)
        print(f"Usuario '{username}' creado exitosamente con contraseña segura.")
        return True
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
        return False