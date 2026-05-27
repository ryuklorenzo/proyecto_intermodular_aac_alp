from pydantic import BaseModel

class ReconocimientoImport(BaseModel):
    detalle: str


class ReconocimientoOut(ReconocimientoImport):
    id: int
    id_actitud: int