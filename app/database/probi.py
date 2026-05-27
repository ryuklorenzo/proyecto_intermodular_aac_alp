from app.database.database_config import db_config
from app.models import probi
from app.models.probi import ProbiImport, ProbiOut
import mariadb

#--------------------------------------------------- PROBI ---------------------------------------------------
def insert_probi(id_mencion: int , probi: ProbiImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO PROBI (fecha, id_mencion)
        VALUES (?, ?)
        """
        values = (probi.fecha, id_mencion)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando probi: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_probis() -> list[ProbiOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, fecha, id_mencion
        FROM PROBI
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        probis = []
        for row in results:
            probis.append(
                ProbiOut(
                    id=row[0],
                    fecha=row[1],
                    id_mencion=row[2]
                )
            )
        return probis
        
    except mariadb.Error as e:
        print(f"Error leyendo Probis: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_probi_by_id(id: int) -> ProbiOut | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        SELECT id, fecha, id_mencion
        FROM PROBI
        WHERE id = ?
        """

        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return ProbiOut(
                id=row[0],
                fecha=row[1],
                id_mencion=row[2]
            )

        return None

    except mariadb.Error as e:
        print(f"Error leyendo probi: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def update_probi(id: int, probi: ProbiImport, id_mencion: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM MENCION WHERE id = ?", (id_mencion,))
        if not cursor.fetchone():
            print(f"Error: El horario con id {id_mencion} no existe.")
            return False

        sql = """
        UPDATE PROBI
        SET fecha = ?, id_mencion = ?
        WHERE id = ?
        """
        values = (probi.fecha, id_mencion, id)
        
        cursor.execute(sql, values)
        conn.commit()

        # Retornamos True solo si se encontró y actualizó el registro
        return True

    except mariadb.Error as e:
        print(f"Error actualizando probi: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def delete_probi(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "DELETE FROM PROBI WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando probi: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
