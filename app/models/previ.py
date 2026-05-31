from datetime import date
from pydantic import BaseModel

class PreviImport(BaseModel):
    detalle: str
    fecha: date

class PreviOut(PreviImport):
    id : int
    id_directivo: int
    id_expediente: int