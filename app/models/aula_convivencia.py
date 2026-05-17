from pydantic import BaseModel

class AulaConvivenciaImport(BaseModel):
    nombre: str
    fecha: str
    id_horario: int

class AulaConvivenciaOut(AulaConvivenciaImport):
    id: int