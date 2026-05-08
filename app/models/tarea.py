from pydantic import BaseModel

class TareaBase(BaseModel):
    descripcion: str
    estado: str

class TareaCreate(TareaBase):
    id_profesor: int
    id_alumno: int

class TareaOut(TareaBase):
    id: int