from pydantic import BaseModel

class AulaConvivenciaAlumnoImport(BaseModel):
    id_aulo_convivencia: int
    alumnos_ids: list[int]