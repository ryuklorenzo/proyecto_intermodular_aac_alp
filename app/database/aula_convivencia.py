from app.database.database_config import db_config
from app.models import aula_convivencia
from app.models.aula_convivencia import AulaConvivenciaImport, AulaConvivenciaOut
from app.models.aula_convivencia_alumno import AulaConvivenciaAlumnoImport
import mariadb

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
        
        sql = """
        SELECT 
            a.id, a.nombre, a.fecha, 
            h.id, h.formato, h.hora_inicio, h.hora_fin 
        FROM AULA_CONVIVENCIA a
        JOIN HORARIO h ON a.id_horario = h.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        aulas = []
        for row in results:
            aulas.append(
                AulaConvivenciaOut(
                    id=row[0],
                    nombre=row[1],
                    fecha=row[2],
                    id_horario=row[3],     # h.id
                    formato=str(row[4]),   # h.formato (Aquí daba el IndexError)
                    hora_inicio=str(row[5]), # h.hora_inicio
                    hora_fin=str(row[6])     # h.hora_fin
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
        SELECT 
            a.id, a.nombre, a.fecha, 
            h.id, h.formato, h.hora_inicio, h.hora_fin 
        FROM AULA_CONVIVENCIA a
        JOIN HORARIO h ON a.id_horario = h.id
        WHERE a.id = ?
        """

        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            # Mapeamos cada columna al modelo AulaConvivenciaOut
            return AulaConvivenciaOut(
                id=row[0],
                nombre=row[1],
                fecha=row[2],
                id_horario=row[3],     # h.id
                formato=str(row[4]),   # h.formato
                hora_inicio=str(row[5]), # h.hora_inicio
                hora_fin=str(row[6])     # h.hora_fin
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