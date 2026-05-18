from pydantic import BaseModel

class PreviImport(BaseModel):
    detalle: str
    fecha: str

class PreviOut(PreviImport):
    id : int
    id_directivo: int
    id_expediente: int