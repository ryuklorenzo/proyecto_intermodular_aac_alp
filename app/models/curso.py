from pydantic import BaseModel

class CursoCreate(BaseModel):
    nivel: str
    curso: str
    modulo: str
    id_horario: int

class CursoOut(CursoCreate):
    id:int