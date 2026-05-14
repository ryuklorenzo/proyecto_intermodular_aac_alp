from pydantic import BaseModel

class CursoCreate(BaseModel):
    nivel: str
    curso: str
    modulo: str

class CursoOut(BaseModel):
    id:int
    nivel: str
    curso: str
    modulo: str
    formato: str
    hora_inicio: str
    hora_fin: str