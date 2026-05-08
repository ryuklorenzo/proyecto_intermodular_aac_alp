from app.database.database_config import db_config
from app.models.horario import HorarioImport, HorarioOut
import mariadb

#--------------------------------------------------- HORARIOS ---------------------------------------------------
def insert_horario(horario: HorarioImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO HORARIO (dia, horario_inicio, horario_fin)
        VALUES (?, ?)
        """
        values = (horario.dia, horario.horario_inicio, horario.horario_fin)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando horario: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_horarios() -> list[HorarioOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, dia, horario_inicio, horario_fin FROM HORARIO
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        horarios = []
        for row in results:
            horarios.append(
                HorarioOut(
                    id=row[0],
                    dia=row[1],
                    horario_inicio=row[2],
                    horario_fin=row[3]
                )
            )
        return horarios
        
    except mariadb.Error as e:
        print(f"Error leyendo horarios: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_horario(id: int, horario: HorarioImport) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        UPDATE HORARIO
        SET dia = ?, horario_inicio = ?, horario_fin = ?
        WHERE id = ?
        """
        values = (
            horario.dia,
            horario.horario_inicio,
            horario.horario_fin,
            id
        )

        cursor.execute(sql, values)
        conn.commit()

        return cursor.rowcount > 0 #1 si se actualizo algo

    except mariadb.Error as e:
        print(f"Error actualizando horario: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_horario(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "DELETE FROM HORARIO WHERE id = ?"
        cursor.execute(sql, (id,))
        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando actitud: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
