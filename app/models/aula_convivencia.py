from datetime import date

from pydantic import BaseModel


class AulaConvivenciaImport(BaseModel):
    nombre: str
    fecha: date

class AulaConvivenciaOut(AulaConvivenciaImport):
    id: int
    id_horario: int
    formato: str
    hora_inicio: str
    hora_fin: str