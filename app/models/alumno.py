from app.models.user import UserBase, UserOut

class AlumnoCreate(UserBase):
    curso: str 

class AlumnoOut(UserOut):
    id: int
    curso: str
    pass