from app.models import UserDb, UserIn, UserBase
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

#---------------------------------------_FUNCIONES USER------------------------------------------------------------
def insert_user(user: UserDb) -> int:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO USUARIO (nombre, username, password) VALUES (?, ?, ?)"
        values = (user.name, user.username, user.password)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        return last_id
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise e

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
            user = UserDb(
                id=row[0], 
                name=row[1],
                username=row[2], 
                password=row[3]
            )
            users_db.append(user)
            
        cursor.close()
        conn.close()
        return users_db
        
    except mariadb.Error as e:
        print(f"Error reading users: {e}")
        return []

def deleteUser(user: UserBase) -> bool:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # 1. Primero buscamos la contraseña hasheada de ese usuario
        sql_check = "SELECT password FROM USUARIO WHERE username = ?"
        cursor.execute(sql_check, (user.username,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            print("No existe ese usuario")
            return False # El usuario no existe
        stored_hash = result[0]

        # 2. Comprobamos si la contraseña que nos pasan coincide con el hash de la BD
        if verify_password(user.password, stored_hash):
            # 3. Si coincide, procedemos a borrar
            sql_delete = "DELETE FROM USUARIO WHERE username = ?"
            cursor.execute(sql_delete, (user.username,))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            print("Contraseña no es correcta")
            return False # La contraseña no es correcta

    except mariadb.Error as e:
        print(f"Error deleting user: {e}")
        return False

def read_user_by_id(id: int) -> UserDb | None:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Seleccionamos los datos filtrando por ID
        sql = "SELECT id, nombre, username, password FROM USUARIO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
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

