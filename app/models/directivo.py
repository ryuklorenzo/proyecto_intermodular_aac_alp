from pydantic import BaseModel
from .user import UserOut

class DirectivoImport(BaseModel):
    cargo: str

class DirectivoOut(UserOut):
    cargo: str