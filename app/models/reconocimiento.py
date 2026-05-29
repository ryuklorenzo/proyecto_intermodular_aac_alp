from datetime import date
from pydantic import BaseModel

class ReconocimientoImport(BaseModel):
    detalle: str


class ReconocimientoOut(ReconocimientoImport):
    id: int
    id_actitud: int
    
    actitud_descripcion: str
    actitud_fecha: date
    actitud_tipo: str