from app.models import UserDb, UserIn, UserBase
from app.models import AlumnoCreate, AlumnoDb
from app.auth.auth import verify_password, get_hash_password
import mariadb

db_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

usersAdmins : list[UserDb] = [
    UserDb(
        id=1,
        name="luffy",
        username="luffy",
        password="$2b$12$QNDLTj7xe8Sl2qMXpj0nNeGds4e79922CGaC00482dcpooo2vW3kW"
        ),
    UserDb(
        id=2,
        name="zoro",
        username="zoro",
        password="$2b$12$IATg6PFpDn6eTHD8nMhbAecOpvQNieFCm36SNwNddGNMeCbzmdHMO"
        ),
    UserDb(
        id=3,
        name="azael",
        username="azael",
        password=get_hash_password("azael")
    ),
    UserDb(
        id=4,
        name="angel",
        username="angel",
        password=get_hash_password("angel")
    )
]

#---------------------------------------_FUNCIONES_USER_------------------------------------------------------------
def insert_user(user: UserDb) -> int:
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
        raise e
    finally:
        # Esto asegura que la conexión se cierre SIEMPRE, incluso si hubo error
        if conn:
            conn.close()
        if cursor:
            cursor.close()

def read_all_users() -> list[UserDb]:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Seleccionamos id, nombre, username y password
        sql = "SELECT id, nombre, username, password FROM USUARIO"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        users_db = []
        for row in results:
            # Mapeamos los resultados de la BD al modelo UserDb
            # row[0]=id, row[1]=nombre, row[2]=username, row[3]=password
            user = UserDb(
                id=row[0], 
                name=row[1],       # En BD es 'nombre', en modelo es 'name'
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

#---------------------------------------_FUNCIONES_ROOT_------------------------------------------------------------


#---------------------------------------_FUNCIONES_ALUMNO_------------------------------------------------------------

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

