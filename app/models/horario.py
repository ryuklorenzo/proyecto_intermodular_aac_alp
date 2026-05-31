from datetime import time
from pydantic import BaseModel, Field

class HorarioImport(BaseModel):
    formato: str = Field(examples=["Presencial"])
    hora_inicio: time = Field(examples=["08:00:00"])
    hora_fin: time = Field(examples=["18:30:00"])

class HorarioOut(HorarioImport):
    id: int