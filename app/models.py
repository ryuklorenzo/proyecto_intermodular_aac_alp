from pydantic import BaseModel

#Usuario base
class UserBase(BaseModel):
    username : str
    password : str

class UserIn(UserBase):
    name : str 

# Los datos de los usuarios se almacenan en la bsae de datos
class UserDb(UserIn):
    id: int 
    
class UserOut(BaseModel):
    id: int
    name: str
    username: str

# Formato de respuesta al iniciar sesión
class TokenOut(BaseModel):
    token: str


class UserLoginIn(UserBase):
    pass