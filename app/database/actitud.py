from app.models.actitud import ActitudCreate, ActitudOut
from app.auth.auth import db_config
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


def read_actitudes_by_alumno(id_usuario: int) -> list[ActitudOut]:
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


def delete_actitud(id: int) -> tuple[bool, str]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # Comprobamos si existe primero
        cursor.execute("SELECT id FROM ACTITUD WHERE id = ?", (id,))
        if not cursor.fetchone():
            return False, "not_found"

        sql = "DELETE FROM ACTITUD WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()

        return True, "ok"

    except mariadb.Error as e:
        print(f"Error borrando actitud: {e}")
        return False, str(e)

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
