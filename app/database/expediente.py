from app.auth.auth import db_config
from app.models.expediente import ExpedienteImport, ExpedienteOut
import mariadb


BASE_SQL_QUERY = """
    SELECT 
        e.id, 
        e.estado, 
        e.id_alumno, 
        e.id_directivo,
        ua.nombre, 
        ua.apellidos,
        ud.nombre, 
        ud.apellidos, 
        d.cargo
    FROM EXPEDIENTE e
    JOIN USUARIO ua ON e.id_alumno = ua.id
    JOIN USUARIO ud ON e.id_directivo = ud.id
    JOIN DIRECTIVO d ON e.id_directivo = d.id
"""

def map_expediente_row(row) -> ExpedienteOut:
    return ExpedienteOut(
        id=row[0],
        estado=row[1],
        id_alumno=row[2],
        id_directivo=row[3],
        nombre_alumno=row[4],
        apellidos_alumno=row[5],
        nombre_directivo=row[6],
        apellidos_directivo=row[7],
        cargo_directivo=row[8]
    )

#--------------------------------------------------- EXPEDIENTES ---------------------------------------------------
def insert_expediente(id_alumno: int, id_directivo: int, expediente: ExpedienteImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO EXPEDIENTE (estado, id_alumno, id_directivo)
        VALUES (?, ?, ?)
        """
        values = (expediente.estado, id_alumno, id_directivo)

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
        """ + BASE_SQL_QUERY
        cursor.execute(sql)
        results = cursor.fetchall()
        
        return [map_expediente_row(row) for row in results]
        
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

        sql = BASE_SQL_QUERY + " WHERE e.id_directivo = ?"
        cursor.execute(sql, (id_directivo,))
        results = cursor.fetchall()

        return [map_expediente_row(row) for row in results]

    except mariadb.Error as e:
        print(f"Error leyendo expedientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_expediente_by_alumno(id_alumno: int) -> list[ExpedienteOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = BASE_SQL_QUERY + " WHERE e.id_alumno = ?"
        cursor.execute(sql, (id_alumno,))
        results = cursor.fetchall()

        return [map_expediente_row(row) for row in results]

    except mariadb.Error as e:
        print(f"Error leyendo expedientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()