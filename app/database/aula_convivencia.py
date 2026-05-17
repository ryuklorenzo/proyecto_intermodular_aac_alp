from app.database.database_config import db_config
from app.models import aula_convivencia
from app.models.aula_convivencia import AulaConvivenciaImport, AulaConvivenciaOut
import mariadb

#--------------------------------------------------- AULA_CONVIVENCIA ---------------------------------------------------
def insert_aula_convivencia(aula: AulaConvivenciaImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO AULA CONVIVENCIA (nombre, fecha, id_horario)
        VALUES (?, ?, ?)
        """
        values = (aula.nombre, aula.fecha, aula.id_horario)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando aula de convivencia: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_aulas_convivencia() -> list[AulaConvivenciaOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, nombre, fecha, id_horario FROM AULA_CONVIVENCIA
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        aulas = []
        for row in results:
            aulas.append(
                AulaConvivenciaOut(
                    id=row[0],
                    nombre=row[1],
                    fecha=str(row[2]),
                    id_horario=(row[3])
                )
            )
        return aulas
        
    except mariadb.Error as e:
        print(f"Error leyendo aulas convivencia: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_aula_convivencia_by_id(id: int) -> AulaConvivenciaOut | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        SELECT id, nombre, fecha, id_horario
        FROM AULA_CONVIVENCIA
        WHERE id = ?
        """

        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return AulaConvivenciaOut(
                id=row[0],
                nombre=row[1],
                fecha=str(row[2]),
                id_horario=row[3]
            )

        return None

    except mariadb.Error as e:
        print(f"Error leyendo aula de convivencia: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def update_aula_convivencia(id: int, aula: AulaConvivenciaImport) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        UPDATE AULA_CONVIVENCIA
        SET nombre = ?, fecha = ?, id_horario = ?
        WHERE id = ?
        """
        values = (
            aula.nombre,
            aula.fecha,
            aula.id_horario,
            id
        )

        cursor.execute(sql, values)
        conn.commit()

        return cursor.rowcount > 0 #1 si se actualizo algo

    except mariadb.Error as e:
        print(f"Error actualizando aula de convivencia: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_aula_convivencia(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "DELETE FROM AULA_CONVIVENCIA WHERE id = ?"
        cursor.execute(sql, (id,))
        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando aula de convivencia: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
