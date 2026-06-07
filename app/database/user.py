from app.models.user import UserDb, UserBase
from app.auth.auth import db_config, get_hash_password
import mariadb

# --------------------------------------------------- USERS ---------------------------------------------------
def insert_user(user: UserDb) -> int:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        hashed_password = get_hash_password(user.password)
        sql = "INSERT INTO USUARIO (nombre, apellidos, activo, password) VALUES (?, ?, ?, ?)"
        values = (user.nombre, user.apellidos,user.activo, hashed_password)
        
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


def get_user_for_login(username: str):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT 
            u.id, 
            u.nombre,
            u.apellidos,
            u.password, 
            u.activo,
            CASE
                WHEN r.id IS NOT NULL THEN 'admin'
                WHEN d.id IS NOT NULL THEN 'directivo'
                WHEN p.id IS NOT NULL THEN 'profesor'
                WHEN a.id IS NOT NULL THEN 'alumno'
                ELSE 'none'
            END as rol
        FROM USUARIO u
        LEFT JOIN ROOT r ON u.id = r.id
        LEFT JOIN DIRECTIVO d ON u.id = d.id
        LEFT JOIN PROFESOR p ON u.id = p.id
        LEFT JOIN ALUMNO a ON u.id = a.id
        WHERE u.nombre = ?
        """
        
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        
        if row:
            return {
                "id": row[0],
                "nombre": row[1],
                "apellidos": row[2],
                "password": row[3],
                "activo": bool(row[4]),
                "rol": row[5]
            }
        return None
        
    except mariadb.Error as e:
        print(f"Error buscando usuario para login: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()