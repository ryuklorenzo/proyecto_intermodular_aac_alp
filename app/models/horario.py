from pydantic import BaseModel

class HorarioImport(BaseModel):
    dia: str
    horario_inicio: str
    horario_fin: str

class HorarioOut(HorarioImport):
    id: int