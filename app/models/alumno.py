from app.models.user import UserBase, UserOut

class AlumnoCreate(UserBase):
    id_curso: int 

class AlumnoOut(UserOut):
    id: int
    id_curso: int
    curso: str
    modulo: str