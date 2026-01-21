from pydantic import BaseModel

#-------------------------------MODELS_USERS-----------------------------
#Usuario base
class UserBase(BaseModel):
    nombre : str
    apellidos : str
    activo : bool = True
    password : str

# Los datos de los usuarios se almacenan en la bsae de datos
class UserDb(UserBase):
    id: int

class UserOut(BaseModel):
    id: int
    nombre: str
    apellidos: str
    activo: bool

# Formato de respuesta al iniciar sesión
class TokenOut(BaseModel):
    token: str

class UserLoginIn(UserBase):
    pass

'''#-------------------------------MODELS_ROOTS-----------------------------

class RootBase(BaseModel):
    name : str
    code: str

class RootIn(BaseModel):
    code: str
    name: str

class RootDb(RootBase):
    id: int

class RootOut(RootDb):
    pass'''

#-------------------------------MODELS_ALUMNOS-----------------------------
class AlumnoCreate(BaseModel):
    id: int  # Necesario para vincular con la tabla USUARIO
    curso: bool = True

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
    id_profesor: int
    cargo: str

class DirectivoDb(BaseModel):
    id: int
    nombre: str
    apellidos: str
    activo: bool
    id_profesor: int
    cargo: str