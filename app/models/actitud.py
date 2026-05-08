from pydantic import BaseModel
from datetime import date

class ActitudBase(BaseModel):
    descripcion: str
    fecha: date
    tipo: str

class ActitudCreate(ActitudBase):
    pass

class ActitudOut(ActitudBase):
    id: int
    id_usuario: int