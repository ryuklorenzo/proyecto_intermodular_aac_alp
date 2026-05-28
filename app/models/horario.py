from datetime import time
from pydantic import BaseModel

class HorarioImport(BaseModel):
    formato: str
    hora_inicio: time
    hora_fin: time

class HorarioOut(HorarioImport):
    id: int