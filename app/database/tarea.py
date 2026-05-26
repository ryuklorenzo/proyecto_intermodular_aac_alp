from app.database.database_config import db_config
from app.models.tarea import TareaCreate
import mariadb

#--------------------------------------------------- TAREAS ---------------------------------------------------
def insert_tarea(tarea: TareaCreate) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO TAREA (descripcion, estado, id_profesor, id_alumno)
        VALUES (?, ?, ?, ?)
        """
        values = (tarea.descripcion, tarea.estado, tarea.id_profesor, tarea.id_alumno)

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
