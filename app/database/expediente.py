from app.database.database_config import db_config
from app.models.expediente import ExpedienteImport, ExpedienteOut
import mariadb

#--------------------------------------------------- EXPEDIENTES ---------------------------------------------------
def insert_expediente(id_directivo: int,expediente: ExpedienteImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO EXPEDIENTE (estado, id_directivo)
        VALUES (?, ?)
        """
        values = (expediente.estado, id_directivo)

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
        SELECT id, estado, id_directivo FROM EXPEDIENTE
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        expedientes = []
        for row in results:
            expedientes.append(
                ExpedienteOut(
                    id=row[0],
                    estado=row[1],
                    id_directivo=row[2]
                )
            )
        return expedientes
        
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

        sql = "SELECT id, estado, id_directivo FROM EXPEDIENTE WHERE id_directivo = ?"
        cursor.execute(sql, (id_directivo,))
        results = cursor.fetchall()

        return [ 
            ExpedienteOut(
                id=row[0],
                estado=row[1],
                id_directivo=row[2]
            )
            for row in results
        ]

    except mariadb.Error as e:
        print(f"Error leyendo expedientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

