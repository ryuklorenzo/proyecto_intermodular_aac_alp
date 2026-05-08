from app.database.profesor import read_profesor_by_id
from app.database.database_config import db_config
from app.models.directivo import DirectivoImport, DirectivoOut
import mariadb

#--------------------------------------------------- DIRECTIVOS ---------------------------------------------------
def insert_directivo(id_profesor: int, directivo: DirectivoImport) -> int:
    conn = None
    cursor = None

    try:
        # Obtener datos del profesor
        profesor = read_profesor_by_id(id_profesor)
        if not profesor:
            print("Profesor no encontrado")
            return -1

        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO DIRECTIVO (id, cargo)
        VALUES (?, ?)
        """
        values = (
            profesor.id,
            directivo.cargo
        )

        cursor.execute(sql, values)
        conn.commit()
        return profesor.id

    except mariadb.Error as e:
        print(f"Error insertando directivo: {e}")
        return -1

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def read_all_directivos() -> list[DirectivoOut]:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT u.id, u.nombre, u.apellidos, u.activo, d.cargo
        FROM DIRECTIVO d
        JOIN PROFESOR p ON d.id = p.id
        JOIN USUARIO u ON p.id = u.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        directivos = []
        for row in results:
            directivos.append(
                DirectivoOut(
                    id=row[0],
                    nombre=row[1],
                    apellidos=row[2],
                    activo=bool(row[3]),
                    cargo=row[4]
                    )
            )
        return directivos
        
    except mariadb.Error as e:
        print(f"Error leyendo directivos: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_directivo_by_id(id: int) -> DirectivoOut | None:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        SELECT u.id, u.nombre, u.apellidos, u.activo, d.cargo
        FROM DIRECTIVO d
        JOIN PROFESOR p ON d.id = p.id
        JOIN USUARIO u ON p.id = u.id
        WHERE id = ?
        """ 
        
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        if row:
            return DirectivoOut(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3]),
                cargo=row[4],
                id_profesor=row[5]
            )
        return None
        
    except mariadb.Error as e:
        print(f"Error leyendo directivo por id: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_directivo(id: int) -> bool:
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql_delete = "DELETE FROM DIRECTIVO WHERE id = ?"
        cursor.execute(sql_delete, (id,))
        conn.commit()

        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando directivo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def directivo_exists(id_profesor: int, cargo: str) -> bool:

    conn = None
    cursor = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT id, cargo FROM DIRECTIVO WHERE id = ?"
        cursor.execute(sql, (id_profesor, cargo))

        return cursor.fetchone() is not None

    except mariadb.Error as e:
        print(f"Error comprobando directivo: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

