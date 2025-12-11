from app.models import UserDb, UserIn, UserBase
from app.auth.auth import verify_password
import mariadb

db_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

def insert_user(user: UserDb) -> int:
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Corrección: Tabla 'USUARIO' y columnas según schema.sql
        # Nota: Tu schema tiene 'contraseña' (varchar 50) y 'password' (varchar 100).
        # Usaremos 'password' para el hash seguro y repetiremos el valor en 'contraseña' 
        # para cumplir el NOT NULL de tu esquema actual.
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
        # Es importante relanzar el error para que el endpoint lo capture
        raise e


def get_user_by_password(username:str) -> UserDb | None:
    return None

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

usersAdmins : list[UserDb] = [
    UserDb(id=1,
        name="luffy",
        username="luffy",
        password="$2b$12$QNDLTj7xe8Sl2qMXpj0nNeGds4e79922CGaC00482dcpooo2vW3kW"),
    UserDb(id=2,
        name="zoro",
        username="zoro",
        password="$2b$12$IATg6PFpDn6eTHD8nMhbAecOpvQNieFCm36SNwNddGNMeCbzmdHMO")
]