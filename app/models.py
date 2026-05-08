# from datetime import date
# from pydantic import BaseModel

# from app.routers import horario

# #-------------------------------MODELS_USERS-----------------------------
# #Usuario base
# class UserBase(BaseModel):
#     nombre : str
#     apellidos : str
#     activo : bool = True
#     password : str

# # Los datos de los usuarios se almacenan en la bsae de datos
# class UserDb(UserBase):
#     id: int

# class UserOut(BaseModel):
#     id: int
#     nombre: str
#     apellidos: str
#     activo: bool

# # Formato de respuesta al iniciar sesión
# class TokenOut(BaseModel):
#     token: str

# class UserLoginIn(UserBase):
#     pass

# #-------------------------------MODELS_ALUMNOS-----------------------------
# class AlumnoCreate(UserBase):
#     curso: str 

# class AlumnoOut(UserOut):
#     id: int
#     curso: str
#     pass

# #-------------------------------MODELS_PROFESORES-----------------------------
# class ProfesorImport(UserBase):
#     pass

# class ProfesorOut(UserOut):
#     pass


# #-------------------------------MODELS_DIRECTIVOS-----------------------------
# class DirectivoImport(BaseModel):
#     cargo: str

# class DirectivoOut(UserOut):
#     cargo: str
#     pass


# #-------------------------------MODELS_ACTITUDES-----------------------------
# class ActitudBase(BaseModel):
#     descripcion: str
#     fecha: date
#     tipo: str


# class ActitudCreate(ActitudBase):
#     pass


# class ActitudOut(ActitudBase):
#     id: int
#     id_usuario: int


# #-------------------------------MODELS_TAREAS-----------------------------

# class TareaBase(BaseModel):
#     descripcion: str
#     estado: str

# class TareaCreate(TareaBase):
#     id_profesor: int
#     id_alumno: int

# class TareaOut(TareaBase):
#     id: int


# #-------------------------------MODELS_EXPEDIENTES-----------------------------
# class ExpedienteImport(BaseModel):
#     estado: str

# class ExpedienteOut(ExpedienteImport):
#     id: int
#     id_directivo: int


# #-------------------------------MODELS_HORARIOS-----------------------------
# class HorarioImport(BaseModel):
#     dia: str
#     horario_inicio: str
#     horario_fin: str

# class HorarioOut(HorarioImport):
#     id: int