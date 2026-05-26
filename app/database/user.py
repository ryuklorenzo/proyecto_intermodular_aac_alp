from app.models.user import UserDb, UserBase
from app.database.database_config import db_config
import mariadb

# --------------------------------------------------- USERS ---------------------------------------------------
def insert_user(user: UserDb) -> int:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO USUARIO (nombre, apellidos, activo, password) VALUES (?, ?, ?, ?)"
        values = (user.nombre, user.apellidos,user.activo, user.password)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        
        #cursor.close()
        #conn.close()
        return last_id
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        # Es importante relanzar el error para que el endpoint lo capture
        raise e
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()


def get_user_by_password(username:str) -> UserDb | None:
    return None

def read_all_users() -> list[UserDb]:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, activo, password FROM USUARIO"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        users_db = []
        for row in results:
            user = UserDb(
                id=row[0], 
                nombre=row[1],
                apellidos=row[2], 
                activo=row[3],
                password=row[4]
            )
            users_db.append(user)
            
        #cursor.close()
        #conn.close()
        return users_db
        
    except mariadb.Error as e:
        print(f"Error reading users: {e}")
        return []
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def deleteUser(user: UserDb) -> bool:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # 1. Primero buscamos la contraseña hasheada de ese usuario
        sql_delete = "DELETE FROM USUARIO WHERE id = ?"
        cursor.execute(sql_delete, (user.id,))
        conn.commit()
        return True

    except mariadb as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def read_user_by_id(id: int) -> UserDb | None:
    """
    Lee un usuario por su id y devuelve un objeto UserDb.
    """
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Seleccionamos los datos filtrando por ID
        sql = "SELECT id, nombre, apellidos, activo, password FROM USUARIO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return UserDb(
                id=row[0], 
                nombre=row[1], 
                apellidos=row[2], 
                activo=row[3],
                password=row[4]
            )
        return None

    except mariadb.Error as e:
        print(f"Error leyendo usuario por id: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
