from datetime import date
from pydantic import BaseModel

class MencionImport(BaseModel):
    fecha: date


class MencionOut(MencionImport):
    id: int
    
    id_reconocimiento: int
    detalle_reconocimiento: str
    
    id_actitud: int
    descripcion_actitud: str
    fecha_actitud: date
    tipo_actitud: str