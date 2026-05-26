from pydantic import BaseModel
from app.models.actitud import ActitudOut, ActitudCreate

class AmonestacionBase(ActitudCreate):
    nivel: str

class AmonestacionOut(AmonestacionBase, ActitudOut):
    id: int