from datetime import date
from pydantic import BaseModel

class AmonestacionBase(BaseModel):
    nivel: str

class AmonestacionOut(AmonestacionBase):
    id: int
    
    actitud_id: int
    actitud_descripcion: str
    actitud_tipo: str
    actitud_fecha: date
    
    usuario_id: int
    usuario_nombre: str
    usuario_apellido: str
    
    profesor_id: int
    profesor_nombre: str
    profesor_apellido: str