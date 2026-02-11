from datetime import date
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
    curso: str 

class AlumnoOut(AlumnoCreate):
    nombre : str
    apellidos : str
    activo : bool = True

#-------------------------------MODELS_PROFESORES-----------------------------
class ProfesorImport(BaseModel):
    id: int

class ProfesorOut(ProfesorImport):
    nombre : str
    apellidos : str
    activo : bool = True


#-------------------------------MODELS_DIRECTIVOS-----------------------------
class DirectivoImport(BaseModel):
    id_profesor: int
    cargo: str

class DirectivoOut(DirectivoImport):
    nombre : str
    apellidos : str
    activo : bool = True


#-------------------------------MODELS_ACTITUDES-----------------------------
class ActitudBase(BaseModel):
    descripcion: str
    fecha: date
    tipo: str


class ActitudCreate(ActitudBase):
    pass


class ActitudOut(ActitudBase):
    id: int
    id_usuario: int


#-------------------------------MODELS_TAREAS-----------------------------

class TareaBase(BaseModel):
    descripcion: str
    estado: str
    id_profesor: int
    id_alumno: int

class TareaCreate(TareaBase):
    pass

class TareaOut(TareaBase):
    id: int
