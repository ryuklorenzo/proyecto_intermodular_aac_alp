from pydantic import BaseModel

class UserBase(BaseModel):
    nombre : str
    apellidos : str
    activo : bool = True
    password : str

# Los datos de los usuarios se almacenan en la base de datos
class UserDb(UserBase):
    id: int

class UserOut(BaseModel):
    id: int
    nombre: str
    apellidos: str
    activo: bool