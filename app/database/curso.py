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
        SELECT 
            c.id, c.nivel, c.curso, c.modulo, 
            h.formato, h.hora_inicio, h.hora_fin 
        FROM CURSO c
        JOIN HORARIO h ON c.id_horario = h.id
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
                    formato=str(row[4]),        # Convertimos a str por seguridad en el JSON
                    hora_inicio=str(row[5]),
                    hora_fin=str(row[6])
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

        sql = """
        SELECT 
            c.id, c.nivel, c.curso, c.modulo, 
            h.formato, h.hora_inicio, h.hora_fin 
        FROM CURSO c
        JOIN HORARIO h ON c.id_horario = h.id
        WHERE c.id = ?
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return CursoOut(
                id=row[0],
                nivel=row[1],
                curso=row[2],
                modulo=row[3],
                formato=str(row[4]),
                hora_inicio=str(row[5]),
                hora_fin=str(row[6])
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

        # verificar si existe el curso antes de actualizar
        cursor.execute("SELECT id FROM CURSO WHERE id = ?", (id,))
        if not cursor.fetchone():
            return False

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
        
        #filas_afectadas = cursor.rowcount
        
        conn.commit()
        
        return True

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
        conn.commit()
        
        filas_afectadas = cursor.rowcount
        print(f"Filas eliminadas: {filas_afectadas}") # Revisa esto en tu terminal
        return filas_afectadas > 0
    #TODO  esta mierda da 404, arreglar a futuro

    except mariadb.Error as e:
        print(f"Error borrando curso: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()