from app.database.database_config import db_config
from app.models import reconocimiento
from app.models.reconocimiento import ReconocimientoImport, ReconocimientoOut
import mariadb

#--------------------------------------------------- RECONOCIMIENTO ---------------------------------------------------
def insert_reconocimiento(id_actitud: int , reconocimiento: ReconocimientoImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO RECONOCIMIENTO (detalle, id_actitud)
        VALUES (?, ?, ?)
        """
        values = (reconocimiento.detalle, id_actitud)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando reconocimiento: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_reconocimientos() -> list[ReconocimientoImport]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, detalle, id_actitud
        FROM RECONOCIMIENTO
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        reconocimientos = []
        for row in results:
            reconocimientos.append(
                ReconocimientoOut(
                    id=row[0],
                    detalle=row[1],
                    id_actitud=row[2]
                )
            )
        return reconocimientos
        
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

        sql = """
        SELECT id, detalle, id_actitud
        FROM RECONOCIMIENTO
        WHERE id = ?
        """

        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return ReconocimientoOut(
                id=row[0],
                detalle=row[1],
                id_actitud=row[2]
            )

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

        sql = """
        SELECT id, detalle, id_actitud
        FROM RECONOCIMIENTO
        WHERE id_actitud = ?
        """
        cursor.execute(sql, (id_actitud,))
        results = cursor.fetchall()

        reconocimientos = []

        for row in results:
            reconocimientos.append(
                ReconocimientoOut(
                    id=row[0],
                    detalle=row[1],
                    id_actitud=row[2]
                )
            )
        return reconocimientos

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
