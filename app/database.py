from app.models import UserDb, UserIn, UserBase
from app.models import AlumnoCreate, AlumnoDb, ProfesorDb, ProfesorCreate
from app.auth.auth import verify_password, get_hash_password
from app.models import UserDb, UserIn, UserBase, RootDb
from app.auth.auth import verify_password
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
        name="angel",
        username="angel",
        password=get_hash_password("angel")),
    UserDb(id=2,
        name="azael",
        username="azael",
        password=get_hash_password("azael"))
]

# --------------------------------------------------- USERS ---------------------------------------------------
def insert_user(user: UserDb) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO USUARIO (nombre, username, password) VALUES (?, ?, ?)"
        values = (user.name, user.username, user.password)
        
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
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Seleccionamos id, nombre, username y password
        sql = "SELECT id, nombre, username, password FROM USUARIO"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        users_db = []
        for row in results:
            user = UserDb(
                id=row[0], 
                name=row[1],
                username=row[2], 
                password=row[3]
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

def deleteUser(user: UserBase) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # 1. Primero buscamos la contraseña hasheada de ese usuario
        sql_check = "SELECT password FROM USUARIO WHERE username = ?"
        cursor.execute(sql_check, (user.username,))
        result = cursor.fetchone()

        if not result:
            #conn.close()
            print("No existe ese usuario")
            return False # El usuario no existe
        stored_hash = result[0]

        # 2. Comprobamos si la contraseña que nos pasan coincide con el hash de la BD
        if verify_password(user.password, stored_hash):
            # 3. Si coincide, procedemos a borrar
            sql_delete = "DELETE FROM USUARIO WHERE username = ?"
            cursor.execute(sql_delete, (user.username,))
            conn.commit()
            #conn.close()
            return True
        else:
            #conn.close()
            print("Contraseña no es correcta")
            return False # La contraseña no es correcta

    except mariadb.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def read_user_by_id(id: int) -> UserDb | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Seleccionamos los datos filtrando por ID
        sql = "SELECT id, nombre, username, password FROM USUARIO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        #cursor.close()
        #conn.close()
        
        if row:
            # Si existe, devolvemos el objeto UserDb
            return UserDb(
                id=row[0], 
                name=row[1], 
                username=row[2], 
                password=row[3]
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

# --------------------------------------------------- ROOTS ---------------------------------------------------

def insert_root(root: RootDb) -> int:
    conn = None
    cursor = None
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
    conn = None
    cursor = None
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
    conn = None
    cursor = None
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
        return False


#--------------------------------------------------- ALUMNOS ---------------------------------------------------
def insert_alumno(alumno: AlumnoCreate) -> int:
    conn = None
    cursor = None
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
    conn = None
    cursor = None
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
    conn = None
    cursor = None
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
    conn = None
    cursor = None
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
        values = (profesor.nombre, profesor.apellidos, profesor.activo)

        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid

        cursor.close()
        conn.close()
        return last_id

    except mariadb.Error as e:
        print(f"Error insertando profesor: {e}")
        raise e


def read_all_profesores() -> list[ProfesorDb]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, curso, activo, id_usuario FROM PROFESOR"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        profesor_db = []
        for row in results:
            profesor = ProfesorDb(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3]), # Convertimos 1/0 a True/False
            )
            profesor_db.append(profesor)
            
        #cursor.close()
        #conn.close()
        return profesor_db
        
    except mariadb.Error as e:
        print(f"Error leyendo profesor: {e}")
        return []
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()


def read_profesor_by_id(id: int) -> ProfesorDb | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, curso, activo, id_usuario FROM PROFESOR WHERE id = ?"
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
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()


def delete_profesor(id: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql_delete = "DELETE FROM PROFESOR WHERE id = ?"
        cursor.execute(sql_delete, (id,))
        conn.commit()

        deleted = cursor.rowcount > 0

        cursor.close()
        conn.close()
        return deleted

    except mariadb.Error as e:
        print(f"Error deleting root: {e}")
        return False


def profesor_exists(nombre: str, apellidos: str) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id FROM PROFESOR WHERE nombre = ? AND apellidos = ?"
        cursor.execute(sql, (nombre, apellidos))
        exists = cursor.fetchone() is not None

        cursor.close()
        conn.close()
        return exists

    except mariadb.Error as e:
        print(f"Error checking profesor: {e}")
        return False
