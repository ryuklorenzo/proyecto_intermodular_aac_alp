from pydantic import BaseModel
from datetime import date

class AulaConvivenciaAlumnoImport(BaseModel):
    id_aula_convivencia: int
    alumnos_ids: list[int]

class AulaConvivenciaAlumnoOut(BaseModel):
    nombre_aula_convivencia: str
    fecha: date
    
    id_alumno: int
    nombre: str
    apellidos: str
    activo: bool
    
    id_curso: int
    nivel: str
    curso: str
    modulo: str