from app.models import UserDb, UserIn
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

users : list[UserDb] = [
    UserDb(id=1,
        name="luffy",
        username="luffy",
        password="$2b$12$QNDLTj7xe8Sl2qMXpj0nNeGds4e79922CGaC00482dcpooo2vW3kW"),
    UserDb(id=2,
        name="zoro",
        username="zoro",
        password="$2b$12$IATg6PFpDn6eTHD8nMhbAecOpvQNieFCm36SNwNddGNMeCbzmdHMO")
]