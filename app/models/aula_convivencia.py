from pydantic import BaseModel

class AulaConvivenciaImport(BaseModel):
    nombre: str
    fecha: str

class AulaConvivenciaOut(AulaConvivenciaImport):
    id: int