from app.database.database_config import db_config
from app.models import mencion
from app.models.mencion import MencionImport, MencionOut
import mariadb

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
        
        sql = """
        SELECT id, fecha, id_reconocimiento
        FROM MENCION
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        menciones = []
        for row in results:
            menciones.append(
                MencionOut(
                    id=row[0],
                    fecha=row[1],
                    id_reconocimiento=row[2]
                )
            )
        return menciones
        
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

        sql = """
        SELECT id, fecha, id_reconocimiento
        FROM MENCION
        WHERE id = ?
        """

        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return MencionOut(
                id=row[0],
                fecha=row[1],
                id_reconocimiento=row[2]
            )

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

        sql = """
        SELECT id, fecha, id_reconocimiento
        FROM MENCION
        WHERE id_reconocimiento = ?
        """
        cursor.execute(sql, (id_reconocimiento,))
        results = cursor.fetchall()

        menciones = []

        for row in results:
            menciones.append(
                MencionOut(
                    id=row[0],
                    fecha=row[1],
                    id_reconocimiento=row[2]
                )
            )
        return menciones

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
