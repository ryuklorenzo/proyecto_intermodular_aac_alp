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
class ProfesorBase(BaseModel):
    nombre: str
    apellidos: str

class ProfesorCreate(ProfesorBase):
    activo: bool = True

class ProfesorDb(ProfesorCreate):
    id: int

class ProfesorOut(ProfesorDb):
    pass

class ProfesorImport(BaseModel):
    nombre: str
    apellidos: str

#-------------------------------MODELS_DIRECTIVOS-----------------------------
class DirectivoBase(BaseModel):
    nombre: str
    apellidos: str
    cargo: str
    id_usuario: int

class DirectivoCreate(DirectivoBase):
    activo: bool = True

class DirectivoDb(DirectivoCreate):
    id: int

class DirectivoOut(DirectivoDb):
    pass

class DirectivoImport(BaseModel):
    nombre: str
    apellidos: str
    cargo: str
    id_usuario: int