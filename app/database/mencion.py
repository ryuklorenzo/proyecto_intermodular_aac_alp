from app.database.database_config import db_config
from app.models import mencion
from app.models.mencion import MencionImport, MencionOut
import mariadb

BASE_QUERY = """
        SELECT m.id, m.fecha, m.id_reconocimiento, r.detalle, a.id, a.descripcion, a.fecha, a.tipo
        FROM MENCION as m
        JOIN RECONOCIMIENTO as r ON m.id_reconocimiento = r.id
        JOIN ACTITUD as a ON r.id_actitud = a.id
        """

def map_mencion_row(row) -> MencionOut:
    return MencionOut(
        id=row[0],
        fecha=row[1],
        id_reconocimiento=row[2],
        detalle_reconocimiento=row[3],
        id_actitud=row[4],
        descripcion_actitud=row[5],
        fecha_actitud=row[6],
        tipo_actitud=row[7]
    )

#--------------------------------------------------- MENCION ---------------------------------------------------
def insert_mencion(id_reconocimiento: int , mencion: MencionImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO MENCION (fecha, id_reconocimiento)
        VALUES (?, ?)
        """
        values = (mencion.fecha, id_reconocimiento)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando mencion: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_menciones() -> list[MencionOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = BASE_QUERY
        cursor.execute(sql)
        results = cursor.fetchall()
        return [map_mencion_row(row) for row in results]
        
    except mariadb.Error as e:
        print(f"Error leyendo menciones: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_mencion_by_id(id: int) -> MencionOut | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = BASE_QUERY + "WHERE m.id = ?"

        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return map_mencion_row(row)
        return None

    except mariadb.Error as e:
        print(f"Error leyendo mencion: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def read_menciones_by_reconocimiento(id_reconocimiento: int) -> list[MencionOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = BASE_QUERY + "WHERE m.id_reconocimiento = ?"
        cursor.execute(sql, (id_reconocimiento,))
        results = cursor.fetchall()
        return [map_mencion_row(row) for row in results]

    except mariadb.Error as e:
        print(f"Error leyendo menciones por reconocimiento: {e}")
        return []

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def update_mencion(id: int, mencion: MencionImport, id_reconocimiento: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM RECONOCIMIENTO WHERE id = ?", (id_reconocimiento,))
        if not cursor.fetchone():
            print(f"Error: El reconocimiento con id {id_reconocimiento} no existe.")
            return False

        sql = """
        UPDATE MENCION
        SET fecha = ?, id_reconocimiento = ?
        WHERE id = ?
        """
        values = (mencion.fecha, id_reconocimiento, id)
        
        cursor.execute(sql, values)
        conn.commit()

        return True

    except mariadb.Error as e:
        print(f"Error actualizando mencion: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def delete_mencion(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "DELETE FROM MENCION WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando mencion: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
