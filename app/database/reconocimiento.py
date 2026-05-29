from app.database.database_config import db_config
from app.models import reconocimiento
from app.models.reconocimiento import ReconocimientoImport, ReconocimientoOut
import mariadb

BASE_QUERY = """
        SELECT r.id, r.detalle, r.id_actitud, a.descripcion, a.fecha, a.tipo
        FROM RECONOCIMIENTO as r
        JOIN ACTITUD as a ON r.id_actitud = a.id
        """

def map_reconocimiento_row(row) -> ReconocimientoOut:
    return ReconocimientoOut(
        id=row[0],
        detalle=row[1],
        id_actitud=row[2],
        actitud_descripcion=row[3],
        actitud_fecha=row[4],
        actitud_tipo=row[5]
    )

#--------------------------------------------------- RECONOCIMIENTO ---------------------------------------------------
def insert_reconocimiento(id_actitud: int , reconocimiento: ReconocimientoImport, id_profesor: int) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO RECONOCIMIENTO (detalle, id_actitud, id_profesor)
        VALUES (?, ?, ?)
        """
        values = (reconocimiento.detalle, id_actitud, id_profesor)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando reconocimiento: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_reconocimientos() -> list[ReconocimientoOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = BASE_QUERY
        cursor.execute(sql)
        results = cursor.fetchall()
        return [map_reconocimiento_row(row) for row in results]
        
    except mariadb.Error as e:
        print(f"Error leyendo reconocimientos: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_reconocimiento_by_id(id: int) -> ReconocimientoOut | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = BASE_QUERY + " WHERE r.id = ?"

        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            return map_reconocimiento_row(row)
        return None

    except mariadb.Error as e:
        print(f"Error leyendo reconocimiento: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def read_reconocimientos_by_actitud(id_actitud: int) -> list[ReconocimientoOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = BASE_QUERY + " WHERE r.id_actitud = ?"
        cursor.execute(sql, (id_actitud,))
        results = cursor.fetchall()

        return [map_reconocimiento_row(row) for row in results]

    except mariadb.Error as e:
        print(f"Error leyendo reconocimientos por actitud: {e}")
        return []

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def update_reconocimiento(id: int, reconocimiento: ReconocimientoImport, id_actitud: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM ACTITUD WHERE id = ?", (id_actitud,))
        if not cursor.fetchone():
            print(f"Error: La actitud con id {id_actitud} no existe.")
            return False

        sql = """
        UPDATE RECONOCIMIENTO
        SET detalle = ?, id_actitud = ?
        WHERE id = ?
        """
        values = (reconocimiento.detalle, id_actitud, id)
        
        cursor.execute(sql, values)
        conn.commit()

        return True

    except mariadb.Error as e:
        print(f"Error actualizando reconocimiento: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def delete_reconocimiento(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "DELETE FROM RECONOCIMIENTO WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando reconocimiento: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
