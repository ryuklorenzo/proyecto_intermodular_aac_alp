from app.database.user import read_user_by_id
from app.models.profesor import ProfesorOut, ProfesorImport
from app.database.database_config import db_config
import mariadb

#--------------------------------------------------- PROFESORES ---------------------------------------------------
def insert_profesor(id_usuario: int) -> int: 
    conn = None
    cursor = None

    try:
        usuario = read_user_by_id(id_usuario)
        if not usuario:
            print(f"Usuario con id {id_usuario} no encontrado")
            return -1

        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO PROFESOR (id)
        VALUES (?)
        """
        values = (
            usuario.id,
        )

        cursor.execute(sql, values)
        conn.commit()
        
        return usuario.id

    except mariadb.Error as e:
        print(f"Error insertando profesor: {e}")
        return -1
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def read_all_profesores() -> list[ProfesorOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        SELECT p.id, u.nombre, u.apellidos, u.activo
        FROM PROFESOR p
        JOIN USUARIO u ON p.id = u.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()

        profesores = [
            ProfesorOut(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3])
            )
            for row in results
        ]
        return profesores

    except mariadb.Error as e:
        print(f"Error leyendo profesores: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_profesor_by_id(id: int) -> ProfesorOut | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # CORRECCIÓN: Hacemos JOIN con USUARIO para obtener nombre y apellidos
        # ya que la tabla PROFESOR solo tiene el ID.
        sql = """
        SELECT p.id, u.nombre, u.apellidos, u.activo
        FROM PROFESOR p
        JOIN USUARIO u ON p.id = u.id
        WHERE p.id = ?
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        if row:
            return ProfesorOut(
                id=row[0],
                nombre=row[1],
                apellidos=row[2],
                activo=bool(row[3])
            )
        return None

    except mariadb.Error as e:
        print(f"Error leyendo profesor por id: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_profesor(id: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql_delete = "DELETE FROM PROFESOR WHERE id = ?"
        cursor.execute(sql_delete, (id,))
        conn.commit()

        return cursor.rowcount > 0

    except mariadb.Error as e:
        print(f"Error borrando profesor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def profesor_exists(id_usuario: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # Al ser una relación 1:1, el ID de la tabla PROFESOR es el ID del usuario
        sql = "SELECT id FROM PROFESOR WHERE id = ?"
        cursor.execute(sql, (id_usuario,))

        return cursor.fetchone() is not None

    except mariadb.Error as e:
        print(f"Error comprobando profesor: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def baja_profesor(id: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        UPDATE USUARIO u
        JOIN PROFESOR a ON u.id = a.id
        SET u.activo = 0
        WHERE a.id = ?
        """
        
        cursor.execute(sql, (id,))
        conn.commit()
        
        return True

    except mariadb.Error as e:
        print(f"Error dando de baja al profesor: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
