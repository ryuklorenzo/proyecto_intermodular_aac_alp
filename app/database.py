from app.models import UserDb
import mariadb

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

def insert_user(user: UserDb)-> int | None :
    with mariadb.connect(**db_config)as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO USUARIO (nombre, username, password) VALUES (?, ?, ?)"
            values = (user.name, user.username, user.password)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

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