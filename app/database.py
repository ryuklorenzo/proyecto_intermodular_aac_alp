from app.models import DirectivoCreate, DirectivoDb, UserDb, UserBase
from app.models import AlumnoCreate, AlumnoDb, ProfesorDb, ProfesorCreate
from app.auth.auth import verify_password, get_hash_password
from app.auth.auth import verify_password, TokenData
from app.auth.auth import  oauth2_scheme, decode_token
from fastapi import APIRouter, Depends, status, HTTPException
import mariadb

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}
usersAdmins : list[UserDb] = [
    UserDb(id=1,
        nombre="angel",
        apellidos="angel",
        activo=1,
        password=get_hash_password("angel")),
    UserDb(id=2,
        nombre="azael",
        apellidos="azael",
        activo=1,
        password=get_hash_password("azael"))
]

def validateIsAdmin(token) -> bool:
    data: TokenData = decode_token(token)
    if data.username not in [u.nombre for u in usersAdmins]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return True

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
        
        '''result = cursor.fetchone()'''

        '''if not result:
            #conn.close()
            print("No existe ese usuario")
            return False # El usuario no existe
        stored_hash = result[0]

        # 2. Comprobamos si la contraseña que nos pasan coincide con el hash de la BD
        if verify_password(user.password, stored_hash):
            # 3. Si coincide, procedemos a borrar
            sql_delete = "DELETE FROM USUARIO WHERE id = ?"
            cursor.execute(sql_delete, (user.id,))
            conn.commit()
            #conn.close()
            return True
        else:
            #conn.close()
            print("Contraseña no es correcta")
            return False # La contraseña no es correcta'''

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
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Seleccionamos los datos filtrando por ID
        sql = "SELECT id, nombre, apellidos, activo, password FROM USUARIO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        #cursor.close()
        #conn.close()
        
        if row:
            # Si existe, devolvemos el objeto UserDb
            return UserDb(
                id=row[0], 
                nombre=row[1], 
                apellidos=row[2], 
                activo=row[3],
                password=row[4]
            )
        return None # Si no existe, devolvemos None
        
    except mariadb.Error as e:
        print(f"Error reading user by id: {e}")
        return None
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

'''# --------------------------------------------------- ROOTS ---------------------------------------------------

def insert_root(root: RootDb) -> int:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO ROOT (name, code) VALUES (?, ?)"
        values = (root.name, root.code)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        return last_id
        
    except mariadb.Error as e:
        print(f"Error inserting root: {e}")
        raise e


def read_all_roots() -> list[RootDb]:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, name, code FROM ROOT"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        roots_db = []
        for row in results:
            root = RootDb(
                id=row[0], 
                name=row[1],
                code=row[2]
            )
            roots_db.append(root)
            
        cursor.close()
        conn.close()
        return roots_db
        
    except mariadb.Error as e:
        print(f"Error reading roots: {e}")
        return []

def delete_root(id: int) -> bool:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql_delete = "DELETE FROM ROOT WHERE id = ?"
        cursor.execute(sql_delete, (id,))
        conn.commit()

        deleted = cursor.rowcount > 0

        cursor.close()
        conn.close()
        return deleted

    except mariadb.Error as e:
        print(f"Error deleting root: {e}")
        return False'''


#--------------------------------------------------- ALUMNOS ---------------------------------------------------
def insert_alumno(alumno: AlumnoCreate) -> int:
    conn = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "INSERT INTO ALUMNO (nombre, apellidos, curso, activo, id_usuario) VALUES (?, ?, ?, ?, ?)"
        values = (alumno.nombre, alumno.apellidos, alumno.curso, alumno.activo, alumno.id_usuario)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        
        cursor.close()
        return last_id
        
    except mariadb.Error as e:
        print(f"Error insertando alumno: {e}")
        raise e
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def read_all_alumnos() -> list[AlumnoDb]:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Seleccionamos todos (puedes añadir un WHERE activo = 1 si solo quieres ver los activos)
        sql = "SELECT id, nombre, apellidos, curso, activo, id_usuario FROM ALUMNO"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        alumnos_db = []
        for row in results:
            alumno = AlumnoDb(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                curso=row[3],
                activo=bool(row[4]), # Convertimos 1/0 a True/False
                id_usuario=row[5]
            )
            alumnos_db.append(alumno)
            
        #cursor.close()
        #conn.close()
        return alumnos_db
        
    except mariadb.Error as e:
        print(f"Error leyendo alumnos: {e}")
        return []
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def read_alumno_by_id(id: int) -> AlumnoCreate | None:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, curso, activo, id_usuario FROM ALUMNO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        #cursor.close()
        #conn.close()
        
        if row:
            return AlumnoCreate(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                curso=row[3],
                activo=bool(row[4]),
                id_usuario=row[5]
            )
        return None
        
    except mariadb.Error as e:
        print(f"Error leyendo alumno por id: {e}")
        return None
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def baja_alumno(id: int) -> bool:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # Actualizamos el campo activo a 0 (False)
        sql = "UPDATE ALUMNO SET activo = 0 WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        
        # Verificamos si se afectó alguna fila
        filas_afectadas = cursor.rowcount
        
        #cursor.close()
        #conn.close()
        
        return filas_afectadas > 0

    except mariadb.Error as e:
        print(f"Error dando de baja al alumno: {e}")
        return False
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

#--------------------------------------------------- PROFESORES ---------------------------------------------------

def insert_profesor(profesor: ProfesorCreate) -> int:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "INSERT INTO PROFESOR (nombre, apellidos, activo) VALUES (?, ?, ?)"
        values = (profesor.nombre, profesor.apellidos, profesor.activo) #FALTA AÑADIR EL ID-USUARIO

        cursor.execute(sql, values)
        conn.commit()

        return cursor.lastrowid

    except mariadb.Error as e:
        print(f"Error insertando profesor: {e}")
        return -1 

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_all_profesores() -> list[ProfesorDb]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, activo FROM PROFESOR"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        profesor_db = []
        for row in results:
            profesor = ProfesorDb(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3])  # 1/0 → True/False
            )
            profesor_db.append(profesor)
            
        return profesor_db
        
    except mariadb.Error as e:
        print(f"Error leyendo profesor: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_profesor_by_id(id: int) -> ProfesorDb | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, activo FROM PROFESOR WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        if row:
            return ProfesorDb(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3])
            )
        return None
        
    except mariadb.Error as e:
        print(f"Error leyendo profesor por id: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def delete_profesor(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql_delete = "DELETE FROM PROFESOR WHERE id = ?"
        cursor.execute(sql_delete, (id,))
        conn.commit()

        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error deleting profesor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def profesor_exists(nombre: str, apellidos: str) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id FROM PROFESOR WHERE nombre = ? AND apellidos = ?"
        cursor.execute(sql, (nombre, apellidos))

        return cursor.fetchone() is not None

    except mariadb.Error as e:
        print(f"Error checking profesor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#--------------------------------------------------- DIRECTIVOS ---------------------------------------------------

def insert_directivo(directivo: DirectivoCreate) -> int:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "INSERT INTO DIRECTIVO (nombre, apellidos, activo, cargo, id_usuario) VALUES (?, ?, ?, ?, ?)"
        values = (directivo.nombre, directivo.apellidos, directivo.activo, directivo.cargo, directivo.id_usuario)

        cursor.execute(sql, values)
        conn.commit()

        return cursor.lastrowid

    except mariadb.Error as e:
        print(f"Error insertando directivo: {e}")
        return -1 

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_all_directivos() -> list[DirectivoDb]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, activo, cargo, id_usuario FROM DIRECTIVO"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        directivo_db = []
        for row in results:
            directivo = DirectivoDb(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3]),  # 1/0 → True/False
                cargo=row[4],
                id_usuario=row[5]
            )
            directivo_db.append(directivo)
            
        return directivo_db
        
    except mariadb.Error as e:
        print(f"Error leyendo directivo: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_directivo_by_id(id: int) -> DirectivoDb | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, activo, cargo, id_usuario FROM DIRECTIVO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        if row:
            return DirectivoDb(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3]),
                cargo=row[4],
                id_usuario=row[5]
            )
        return None
        
    except mariadb.Error as e:
        print(f"Error leyendo directivo por id: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def delete_directivo(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql_delete = "DELETE FROM DIRECTIVO WHERE id = ?"
        cursor.execute(sql_delete, (id,))
        conn.commit()

        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error deleting directivo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def directivo_exists(nombre: str, apellidos: str, cargo: str) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id FROM DIRECTIVO WHERE nombre = ? AND apellidos = ? AND cargo = ?"
        cursor.execute(sql, (nombre, apellidos, cargo))

        return cursor.fetchone() is not None

    except mariadb.Error as e:
        print(f"Error checking directivo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()