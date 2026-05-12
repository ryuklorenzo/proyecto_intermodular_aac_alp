from pydantic import BaseModel
from app.models.user import UserOut

class DirectivoImport(BaseModel):
    cargo: str

class DirectivoOut(UserOut):
    cargo: str