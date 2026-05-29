from pydantic import BaseModel

class ExpedienteImport(BaseModel):
    estado: str

class ExpedienteOut(ExpedienteImport):
    id: int
    id_alumno: int
    id_directivo: int
    
    nombre_alumno: str
    apellidos_alumno: str
    nombre_directivo: str
    apellidos_directivo: str
    cargo_directivo: str