from app.database.database_config import db_config
from app.models.amonestacion import AmonestacionBase, AmonestacionOut
import mariadb

BASE_QUERY = """
    SELECT 
        a.id, 
        a.nivel, 
        
        ac.id, 
        ac.descripcion, 
        ac.tipo,
        ac.fecha, 
        
        u.id, 
        u.nombre, 
        u.apellidos,
        
        p.id, 
        up.nombre, 
        up.apellidos
    FROM AMONESTACION a
    JOIN ACTITUD ac ON a.id_actitud = ac.id
    JOIN USUARIO u ON ac.id_usuario = u.id
    JOIN PROFESOR p ON a.id_profesor = p.id
    JOIN USUARIO up ON p.id = up.id
"""

def map_amonestacion_row(row) -> AmonestacionOut:
    return AmonestacionOut(
        id=row[0],
        nivel=row[1],
        actitud_id=row[2],
        actitud_descripcion=row[3],
        actitud_tipo=row[4],
        actitud_fecha=row[5],
        usuario_id=row[6],
        usuario_nombre=row[7],
        usuario_apellido=row[8],
        profesor_id=row[9],
        profesor_nombre=row[10],
        profesor_apellido=row[11]
    )

def insert_amonestacion(id_actitud: int, amonestacion: AmonestacionBase, id_profesor: int) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "INSERT INTO AMONESTACION (id, nivel, id_actitud, id_profesor) VALUES (?, ?, ?, ?)"
        values = (None, amonestacion.nivel, id_actitud, id_profesor)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        
        return last_id
        
    except mariadb.Error as e:
        print(f"Error insertando amonestacion: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_all_amonestaciones() -> list[AmonestacionOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = BASE_QUERY
        cursor.execute(sql)
        results = cursor.fetchall()
        return [map_amonestacion_row(row) for row in results]
        
    except mariadb.Error as e:
        print(f"Error leyendo amonestaciones: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_amonestacion_by_id(id: int) -> AmonestacionOut | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = BASE_QUERY + " WHERE a.id = ?"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        
        if result:
            return map_amonestacion_row(result)
        else:
            return None
        
    except mariadb.Error as e:
        print(f"Error leyendo amonestacion por id: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_amonestacion_by_userid(id_alumno: int) -> AmonestacionOut | None:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = BASE_QUERY + " WHERE u.id = ?"
        cursor.execute(sql, (id_alumno,))
        results = cursor.fetchall()
        return [map_amonestacion_row(row) for row in results]
        
    except mariadb.Error as e:
        print(f"Error leyendo amonestacion por id: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_amonestacion(id: int) -> bool:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "DELETE FROM AMONESTACION WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        
        return cursor.rowcount > 0
        
    except mariadb.Error as e:
        print(f"Error eliminando amonestacion: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
