from app.models.alumno import AlumnoCreate, AlumnoOut
from app.database.database_config import db_config
import mariadb

#--------------------------------------------------- ALUMNOS ---------------------------------------------------
def insert_alumno(id: int, alumno: AlumnoCreate) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "INSERT INTO ALUMNO (id, id_curso) VALUES (?, ?)"
        values = (id, alumno.id_curso)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        
        return last_id
        
    except mariadb.Error as e:
        print(f"Error insertando alumno: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_all_alumnos() -> list[AlumnoOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT 
            a.id, u.nombre, u.apellidos, u.activo, 
            c.id, c.curso, c.modulo
        FROM ALUMNO a
        JOIN USUARIO u ON a.id = u.id
        JOIN CURSO c ON a.id_curso = c.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        alumnos_db = []
        for row in results:
            alumno = AlumnoOut(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3]),
                id_curso=row[4],
                curso=row[5],
                modulo=row[6]
            )
            alumnos_db.append(alumno)
            
        return alumnos_db
        
    except mariadb.Error as e:
        print(f"Error leyendo alumnos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def read_alumno_by_id(id: int) -> AlumnoOut | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT 
            a.id, u.nombre, u.apellidos, u.activo, 
            c.id, c.curso, c.modulo
        FROM ALUMNO a
        JOIN USUARIO u ON a.id = u.id
        JOIN CURSO c ON a.id_curso = c.id
        WHERE a.id = ?
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        if row:
            return AlumnoOut(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3]),
                id_curso=row[4],
                curso=row[5],
                modulo=row[6]
            )
        return None
        
    except mariadb.Error as e:
        print(f"Error leyendo alumno por id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def baja_alumno(id: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        UPDATE USUARIO u
        JOIN ALUMNO a ON u.id = a.id
        SET u.activo = 0
        WHERE a.id = ?
        """
        
        cursor.execute(sql, (id,))
        conn.commit()
        
        return True

    except mariadb.Error as e:
        print(f"Error dando de baja al alumno: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
