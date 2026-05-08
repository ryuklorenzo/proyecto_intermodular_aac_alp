from app.models.actitud import ActitudCreate, ActitudOut
from app.database.database_config import db_config
import mariadb

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
