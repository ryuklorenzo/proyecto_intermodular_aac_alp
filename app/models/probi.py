from datetime import date
from pydantic import BaseModel

class ProbiImport(BaseModel):
    fecha: date

class ProbiOut(ProbiImport):
    id: int
    id_mencion: int