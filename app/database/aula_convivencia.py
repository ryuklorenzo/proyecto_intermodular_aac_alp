from app.auth.auth import db_config
from app.models import aula_convivencia
from app.models.aula_convivencia import AulaConvivenciaImport, AulaConvivenciaOut
from app.models.aula_convivencia_alumno import AulaConvivenciaAlumnoImport, AulaConvivenciaAlumnoOut
import mariadb

BASE_SQL_QUERY = """
    SELECT 
        ac.id, 
        ac.nombre, 
        ac.fecha, 
        ac.id_horario, 
        h.formato, 
        h.hora_inicio, 
        h.hora_fin
    FROM AULA_CONVIVENCIA ac
    JOIN HORARIO h ON ac.id_horario = h.id
"""

def map_aula_row(row) -> AulaConvivenciaOut:
    return AulaConvivenciaOut(
        id=row[0],
        nombre=row[1],
        fecha=row[2],
        id_horario=row[3],
        formato=row[4],
        hora_inicio=str(row[5]), 
        hora_fin=str(row[6])
    )


#--------------------------------------------------- AULA_CONVIVENCIA ---------------------------------------------------
def insert_aula_convivencia(id_horario: int , aula: AulaConvivenciaImport) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO AULA_CONVIVENCIA (nombre, fecha, id_horario)
        VALUES (?, ?, ?)
        """
        values = (aula.nombre, aula.fecha, id_horario)

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
        
        sql = BASE_SQL_QUERY
        cursor.execute(sql)
        results = cursor.fetchall()
        
        return [map_aula_row(row) for row in results]
        
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

        sql = BASE_SQL_QUERY + " WHERE ac.id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            return map_aula_row(row)
        return None

    except mariadb.Error as e:
        print(f"Error leyendo aula de convivencia: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def update_aula_convivencia(id: int, aula: AulaConvivenciaImport, id_horario: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # 3. VERIFICACIÓN: Comprobar que el horario existe antes de actualizar
        cursor.execute("SELECT id FROM HORARIO WHERE id = ?", (id_horario,))
        if not cursor.fetchone():
            print(f"Error: El horario con id {id_horario} no existe.")
            return False

        sql = """
        UPDATE AULA_CONVIVENCIA
        SET nombre = ?, fecha = ?, id_horario = ?
        WHERE id = ?
        """
        values = (aula.nombre, aula.fecha, id_horario, id)
        
        cursor.execute(sql, values)
        conn.commit()

        # Retornamos True solo si se encontró y actualizó el registro
        return True

    except mariadb.Error as e:
        print(f"Error actualizando aula de convivencia: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def delete_aula_convivencia(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "DELETE FROM AULA_CONVIVENCIA WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando aula de convivencia: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def assign_alumnos_to_aula(id_aula_convivencia: int, alumnos_ids: list[int]) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM AULA_CONVIVENCIA WHERE id = ?", 
            (id_aula_convivencia,)
        )

        if not cursor.fetchone():
            print("Aula no encontrada")
            return False

        sql = """
        INSERT INTO AULA_CONVIVENCIA_ALUMNO
        (id_aula_convivencia, id_alumno)
        VALUES (?, ?)
        """

        for id_alumno in alumnos_ids:

            cursor.execute(
                "SELECT id FROM ALUMNO WHERE id = ?",
                (id_alumno,)
            )

            if cursor.fetchone():
                cursor.execute(
                    sql,
                    (id_aula_convivencia, id_alumno)
                )
        conn.commit()

        return True

    except mariadb.Error as e:
        print(f"Error añadiendo alumno a aula: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_alumnos_in_aula(id_aula_convivencia: int) -> list[AulaConvivenciaAlumnoOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT u.id, u.nombre, u.apellidos, u.activo, a.id_curso, c.nivel, c.curso, c.modulo, ac.nombre, ac.fecha
        FROM AULA_CONVIVENCIA_ALUMNO aca
        JOIN ALUMNO a ON aca.id_alumno = a.id
        JOIN USUARIO u ON a.id = u.id
        JOIN CURSO c ON a.id_curso = c.id
        JOIN AULA_CONVIVENCIA ac ON aca.id_aula_convivencia = ac.id
        WHERE aca.id_aula_convivencia = ?
        """
        cursor.execute(sql, (id_aula_convivencia,))
        results = cursor.fetchall()
        
        alumnos = []
        for row in results:
            alumnos.append(
                AulaConvivenciaAlumnoOut(
                    nombre_aula_convivencia=row[8],
                    fecha=row[9],
                    id_alumno=row[0],
                    nombre=row[1],
                    apellidos=row[2],
                    activo=bool(row[3]),
                    id_curso=row[4],
                    nivel=row[5],
                    curso=row[6],
                    modulo=row[7]
                )
            )
        return alumnos
        
    except mariadb.Error as e:
        print(f"Error leyendo alumnos del aula de convivencia: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def remove_alumno_from_aula(id_aula_convivencia: int, id_alumno: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(
            """SELECT id_alumno FROM AULA_CONVIVENCIA_ALUMNO 
                WHERE id_aula_convivencia = ? AND id_alumno = ?""", 
            (id_aula_convivencia, id_alumno)
        )
        
        if not cursor.fetchone():
            return False

        sql = """
        DELETE FROM AULA_CONVIVENCIA_ALUMNO 
        WHERE id_aula_convivencia = ? AND id_alumno = ?
        """
        cursor.execute(sql, (id_aula_convivencia, id_alumno))
        conn.commit()

        return True

    except mariadb.Error as e:
        print(f"Error sacando al alumno del aula de convivencia: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()