from pydantic import BaseModel

#-------------------------------MODELS_USERS-----------------------------
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

#-------------------------------MODELS_ROOTS-----------------------------

class RootBase(BaseModel):
    name : str
    code: str

class RootIn(BaseModel):
    code: str
    name: str

class RootDb(RootBase):
    id: int

class RootOut(RootDb):
    pass

#-------------------------------MODELS_ALUMNOS-----------------------------
class AlumnoBase(BaseModel):
    nombre: str
    apellidos: str
    curso: str

class AlumnoCreate(AlumnoBase):
    activo: bool = True
    id_usuario: int  # Necesario para vincular con la tabla USUARIO

class AlumnoDb(AlumnoCreate):
    id: int
    pass

#-------------------------------MODELS_PROFESORES-----------------------------
class ProfesorImport(BaseModel):
    id_usuario: int

class ProfesorDb(BaseModel):
    id: int
    nombre: str
    apellidos: str
    activo: bool
    id_usuario: int


#-------------------------------MODELS_DIRECTIVOS-----------------------------
class DirectivoImport(BaseModel):
    id_usuario: int
    cargo: str

class DirectivoDb(BaseModel):
    id: int
    nombre: str
    apellidos: str
    activo: bool
    id_usuario: int
    cargo: str