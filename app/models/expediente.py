from pydantic import BaseModel

class ExpedienteImport(BaseModel):
    estado: str

class ExpedienteOut(ExpedienteImport):
    id: int
    id_alumno: int
    id_directivo: int