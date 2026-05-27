from app.database.database_config import db_config
from app.models.amonestacion import AmonestacionBase, AmonestacionOut
import mariadb

def insert_amonestacion(id_actitud: int, amonestacion: AmonestacionBase) -> int:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "INSERT INTO AMONESTACION (id, nivel, id_actitud) VALUES (?, ?, ?)"
        values = (None, amonestacion.nivel, id_actitud)
        
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


# app/database/amonestacion.py

def read_all_amonestaciones() -> list[AmonestacionOut]:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # 1. Añadimos ac.tipo y cambiamos ac.id_alumno por ac.id_usuario
        sql = """
        SELECT 
            a.id, a.nivel, ac.id, ac.descripcion, ac.fecha, ac.tipo, ac.id_usuario
        FROM AMONESTACION a
        JOIN ACTITUD ac ON a.id_actitud = ac.id
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        amonestaciones_db = []
        for row in results:
            amonestacion = AmonestacionOut(
                id=row[0],               # a.id
                nivel=row[1],            # a.nivel
                # row[2] es ac.id (el id de la actitud), no lo necesitas en el Out a menos que lo definas
                descripcion=row[3],      # ac.descripcion
                fecha=row[4],            # ac.fecha (Pydantic se encarga de pasarlo a Date)
                tipo=row[5],             # ac.tipo (¡Faltaba esto!)
                id_usuario=row[6]        # ac.id_usuario (¡Faltaba esto y lo tenías comentado!)
            )
            amonestaciones_db.append(amonestacion)
        
        return amonestaciones_db
        
    except mariadb.Error as e:
        print(f"Error leyendo amonestaciones: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_amonestacion_by_id(id: int) -> AmonestacionOut:
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        # Actualizar la SQL igual que arriba
        sql = """
        SELECT 
            a.id, a.nivel, ac.id, ac.descripcion, ac.fecha, ac.tipo, ac.id_usuario
        FROM AMONESTACION a
        JOIN ACTITUD ac ON a.id_actitud = ac.id
        WHERE a.id = ?
        """
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        
        if result:
            amonestacion = AmonestacionOut(
                id=result[0],
                nivel=result[1],
                descripcion=result[3],
                fecha=result[4],
                tipo=result[5],          # Añadir
                id_usuario=result[6]     # Descomentar/Añadir
            )
            return amonestacion
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
