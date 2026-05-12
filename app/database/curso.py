from app.database.database_config import db_config
from app.models.curso import CursoCreate, CursoOut
import mariadb

#--------------------------------------------------- CURSOS ---------------------------------------------------
def insert_curso(curso: CursoCreate) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO CURSO (nivel, curso, modulo, id_horario)
        VALUES (?, ?, ?, ?)
        """
        values = (curso.nivel, curso.curso, curso.modulo, curso.id_horario)

        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    
    except mariadb.Error as e:
        print(f"Error insertando curso: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_cursos() -> list[CursoOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT id, nivel, curso, modulo, id_horario FROM CURSO
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        cursos = []
        for row in results:
            cursos.append(
                CursoOut(
                    id=row[0],
                    nivel=row[1],
                    curso=row[2],
                    modulo=row[3],
                    id_horario=row[4]
                )
            )
        return cursos
        
    except mariadb.Error as e:
        print(f"Error leyendo cursos: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_curso_by_id(id: int) -> CursoOut | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, nivel, curso, modulo, id_horario FROM CURSO WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return CursoOut(
                id=row[0],
                nivel=row[1],
                curso=row[2],
                modulo=row[3],
                id_horario=row[4]
            )

        return None

    except mariadb.Error as e:
        print(f"Error leyendo curso: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_curso(id: int, curso: CursoCreate) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        UPDATE CURSO
        SET nivel = ?, curso = ?, modulo = ?, id_horario = ?
        WHERE id = ?
        """
        values = (
            curso.nivel,
            curso.curso,
            curso.modulo,
            curso.id_horario,
            id
        )

        cursor.execute(sql, values)
        conn.commit()

        return cursor.rowcount > 0 #1 si se actualizo algo

    except mariadb.Error as e:
        print(f"Error actualizando curso: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_curso(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "DELETE FROM CURSO WHERE id = ?"
        cursor.execute(sql, (id,))
        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando curso: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()