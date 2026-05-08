from pydantic import BaseModel

class CursoCreate(BaseModel):
    nivel: str
    curso: str
    modulo: str


class CursoOut(CursoCreate):
    id:int