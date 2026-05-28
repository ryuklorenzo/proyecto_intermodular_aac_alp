from app.database.previ import *
from app.models.previ import *
from app.database.database_config import db_config
import mariadb

#--------------------------------------------------- PREVI ---------------------------------------------------
def insert_previ(id_directivo: int, id_expediente: int, previ: PreviImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO PREVI (detalle, fecha, id_expediente, id_directivo)
        VALUES (?, ?, ?, ?)
        """
        values = (previ.detalle, previ.fecha, id_expediente, id_directivo)

        cursor.execute(sql, values)
        conn.commit()
        
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando previ: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_previ_by_expediente(id_expediente: int) -> list[PreviOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, detalle, fecha, id_directivo, id_expediente FROM PREVI
        WHERE id_expediente = ?
        """
        cursor.execute(sql, (id_expediente,))
        results = cursor.fetchall()
        
        previes = []
        for row in results:
            previes.append(
                PreviOut(
                    id=row[0],
                    detalle=row[1],
                    fecha=str(row[2]),
                    id_directivo=row[3],
                    id_expediente=row[4],
                )
            )
        return previes
        
    except mariadb.Error as e:
        print(f"Error leyendo previes: {e}")
        return []

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_previ_by_directivo(id_directivo: int) -> list[PreviOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, detalle, fecha, id_directivo, id_expediente FROM PREVI
        WHERE id_directivo = ?
        """
        cursor.execute(sql, (id_directivo,))
        results = cursor.fetchall()
        
        previes = []
        for row in results:
            previes.append(
                PreviOut(
                    id=row[0],
                    detalle=row[1],
                    fecha=str(row[2]),
                    id_directivo=row[3],
                    id_expediente=row[4],
                )
            )
        return previes
        
    except mariadb.Error as e:
        print(f"Error leyendo previes: {e}")
        return []

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_previes() -> list[PreviOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, detalle, fecha, id_directivo, id_expediente FROM PREVI
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        previes = []
        for row in results:
            previes.append(
                PreviOut(
                    id=row[0],
                    detalle=row[1],
                    fecha=str(row[2]),
                    id_directivo=row[3],
                    id_expediente=row[4],
                )
            )
        return previes
        
    except mariadb.Error as e:
        print(f"Error leyendo previes: {e}")
        return []

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update_previ(id_previ: int, previ: PreviImport) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        UPDATE PREVI
        SET detalle = ?, fecha = ?
        WHERE id = ?
        """
        values = (previ.detalle, previ.fecha, id_previ)

        cursor.execute(sql, values)
        conn.commit()
        
        return True
    
    except mariadb.Error as e:
        print(f"Error actualizando previ: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def delete_previ(id_previ: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "DELETE FROM PREVI WHERE id = ?"
        cursor.execute(sql, (id_previ,))
        conn.commit()
        
        return cursor.rowcount > 0
    
    except mariadb.Error as e:
        print(f"Error eliminando previ: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

