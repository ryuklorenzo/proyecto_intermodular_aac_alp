from app.models import DirectivoImport, DirectivoOut, UserDb, UserBase
from app.models import AlumnoCreate, AlumnoOut, ProfesorOut, ProfesorImport, ActitudCreate, ActitudOut, TareaCreate, TareaOut, ExpedienteImport, ExpedienteOut
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
def insert_alumno(id_usuario: int, alumno: AlumnoCreate) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "INSERT INTO ALUMNO (id, curso) VALUES (?, ?)"
        values = (id_usuario, alumno.curso)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        
        return last_id
        
    except mariadb as e:
        print(f"Error insertando alumno: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_all_alumnos() -> list[AlumnoOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT a.id, a.curso, u.nombre, u.apellidos, u.activo 
        FROM ALUMNO a
        JOIN USUARIO u ON a.id = u.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        alumnos_db = []
        for row in results:
            alumno = AlumnoOut(
                id=row[0],
                curso=row[1],
                nombre=row[2],
                apellidos=row[3],
                activo=bool(row[4])
            )
            alumnos_db.append(alumno)
            
        return alumnos_db
        
    except mariadb.Error as e:
        print(f"Error leyendo alumnos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def read_alumno_by_id(id: int) -> AlumnoOut | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT a.id, a.curso, u.nombre, u.apellidos, u.activo 
        FROM ALUMNO a
        JOIN USUARIO u ON a.id = u.id
        WHERE a.id = ?
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        if row:
            return AlumnoOut(
                id=row[0],
                curso=row[1],
                nombre=row[2],
                apellidos=row[3],
                activo=bool(row[4])
            )
        return None
        
    except mariadb.Error as e:
        print(f"Error leyendo alumno por id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def baja_alumno(id: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        UPDATE USUARIO u
        JOIN ALUMNO a ON u.id = a.id
        SET u.activo = 0
        WHERE a.id = ?
        """
        
        cursor.execute(sql, (id,))
        conn.commit()
        
        return True

    except mariadb.Error as e:
        print(f"Error dando de baja al alumno: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#--------------------------------------------------- PROFESORES ---------------------------------------------------

def insert_profesor(id_usuario: int) -> int: 
    conn = None
    cursor = None

    try:
        usuario = read_user_by_id(id_usuario)
        if not usuario:
            print(f"Usuario con id {id_usuario} no encontrado")
            return -1

        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO PROFESOR (nombre, apellidos, activo, id_usuario)
        VALUES (?, ?, ?, ?)
        """
        values = (
            usuario.nombre,
            usuario.apellidos,
            usuario.activo,
            usuario.id
        )

        cursor.execute(sql, values)
        conn.commit()
        
        return usuario.id

    except mariadb.Error as e:
        print(f"Error insertando profesor: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_profesores() -> list[ProfesorOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        SELECT p.id, u.nombre, u.apellidos, u.activo
        FROM PROFESOR p
        JOIN USUARIO u ON p.id = u.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()

        profesores = [
            ProfesorOut(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3])
            )
            for row in results
        ]
        return profesores

    except mariadb.Error as e:
        print(f"Error leyendo profesores: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_profesor_by_id(id: int) -> ProfesorOut | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # CORRECCIÓN: Hacemos JOIN con USUARIO para obtener nombre y apellidos
        # ya que la tabla PROFESOR solo tiene el ID.
        sql = """
        SELECT p.id, u.nombre, u.apellidos, u.activo
        FROM PROFESOR p
        JOIN USUARIO u ON p.id = u.id
        WHERE p.id = ?
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return ProfesorOut(
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
        print(f"Error borrando profesor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def profesor_exists(id_usuario: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # Al ser una relación 1:1, el ID de la tabla PROFESOR es el ID del usuario
        sql = "SELECT id FROM PROFESOR WHERE id = ?"
        cursor.execute(sql, (id_usuario,))

        return cursor.fetchone() is not None

    except mariadb.Error as e:
        print(f"Error comprobando profesor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#--------------------------------------------------- DIRECTIVOS ---------------------------------------------------

def insert_directivo(id_profesor: int, directivo: DirectivoImport) -> int:
    conn = None
    cursor = None

    try:
        # Obtener datos del profesor
        profesor = read_profesor_by_id(id_profesor)
        if not profesor:
            print("Profesor no encontrado")
            return -1

        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO DIRECTIVO (id, cargo)
        VALUES (?, ?)
        """
        values = (
            profesor.id,
            directivo.cargo
        )

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


# En app/database.py

def read_all_directivos() -> list[DirectivoOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT d.id, u.nombre, u.apellidos, u.activo, d.cargo
        FROM DIRECTIVO d
        JOIN PROFESOR p ON d.id = p.id
        JOIN USUARIO u ON p.id = u.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        directivos = []
        for row in results:
            directivos.append(
                DirectivoOut(
                    id_profesor=row[0],
                    nombre=row[1],
                    apellidos=row[2],
                    activo=bool(row[3]),
                    cargo=row[4]
                )
            )
        return directivos
        
    except mariadb.Error as e:
        print(f"Error leyendo directivos: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_directivo_by_id(id: int) -> DirectivoOut | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, apellidos, activo, cargo, id_profesor FROM DIRECTIVO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        if row:
            return DirectivoOut(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3]),
                cargo=row[4],
                id_profesor=row[5]
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
        print(f"Error borrando directivo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def directivo_exists(id_profesor: int, cargo: str) -> bool:

    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, cargo FROM DIRECTIVO WHERE id = ?"
        cursor.execute(sql, (id_profesor, cargo))

        return cursor.fetchone() is not None

    except mariadb.Error as e:
        print(f"Error comprobando directivo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


#--------------------------------------------------- ACTITUDES ---------------------------------------------------
def insert_actitud(id_usuario: int, actitud: ActitudCreate) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO ACTITUD (descripcion, fecha, tipo, id_usuario)
        VALUES (?, ?, ?, ?)
        """
        values = (actitud.descripcion, actitud.fecha, actitud.tipo, id_usuario)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando actitud: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_actitudes_by_usuario(id_usuario: int) -> list[ActitudOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, descripcion, fecha, tipo, id_usuario FROM ACTITUD WHERE id_usuario = ?"
        cursor.execute(sql, (id_usuario,))
        results = cursor.fetchall()

        return [
            ActitudOut(
                id=row[0],
                descripcion=row[1],
                fecha=row[2],
                tipo=row[3],
                id_usuario=row[4]
            )
            for row in results
        ]

    except mariadb.Error as e:
        print(f"Error leyendo actitudes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_actitud(id_actitud: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, cargo FROM ACTITUD WHERE id = ?"
        cursor.execute(sql, (id_actitud,))

        return cursor.fetchone() is not None

    except mariadb.Error as e:
        print(f"Error comprobando actitud: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


#--------------------------------------------------- TAREAS ---------------------------------------------------
def insert_tarea(id_profesor: int, id_alumno: int, tarea: TareaCreate) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO ACTITUD (descripcion, estado, id_profesor, id_alumno)
        VALUES (?, ?, ?, ?)
        """
        values = (tarea.descripcion, tarea.estado, id_profesor, id_alumno)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando tarea: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_tareas_by_alumno(id_alumno: int) -> list:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, descripcion, estado, id_profesor, id_alumno FROM TAREA WHERE id_alumno = ?"
        cursor.execute(sql, (id_alumno,))
        results = cursor.fetchall()

        return [
            {
                "id": row[0],
                "descripcion": row[1],
                "estado": row[2],
                "id_profesor": row[3],
                "id_alumno": row[4]
            }
            for row in results
        ]

    except mariadb.Error as e:
        print(f"Error leyendo tareas: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_tareas_by_profesor(id_profesor: int) -> list:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, descripcion, estado, id_profesor, id_alumno FROM TAREA WHERE id_profesor = ?"
        cursor.execute(sql, (id_profesor,))
        results = cursor.fetchall()

        return [
            {
                "id": row[0],
                "descripcion": row[1],
                "estado": row[2],
                "id_profesor": row[3],
                "id_alumno": row[4]
            }
            for row in results
        ]

    except mariadb.Error as e:
        print(f"Error leyendo tareas: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#--------------------------------------------------- EXPEDIENTES ---------------------------------------------------
def insert_expediente(id_directivo: int,expediente: ExpedienteImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO EXPEDIENTE (estado, id_directivo)
        VALUES (?, ?)
        """
        values = (expediente.estado, id_directivo)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando expediente: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_expedientes() -> list[ExpedienteOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, estado, id_directivo FROM EXPEDIENTE
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        expedientes = []
        for row in results:
            expedientes.append(
                ExpedienteOut(
                    id=row[0],
                    estado=row[1],
                    id_directivo=row[2]
                )
            )
        return expedientes
        
    except mariadb.Error as e:
        print(f"Error leyendo expedientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_expediente_by_directivo(id_directivo: int) -> list[ExpedienteOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, estado, id_directivo FROM EXPEDIENTE WHERE id_directivo = ?"
        cursor.execute(sql, (id_directivo,))
        results = cursor.fetchall()

        return [
            ExpedienteOut(
                id=row[0],
                estado=row[1],
                id_directivo=row[2]
            )
            for row in results
        ]

    except mariadb.Error as e:
        print(f"Error leyendo expedientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()