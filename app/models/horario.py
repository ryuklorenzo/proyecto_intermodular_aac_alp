from pydantic import BaseModel

class HorarioImport(BaseModel):
    formato: str
    hora_inicio: str
    hora_fin: str

class HorarioOut(HorarioImport):
    id: int