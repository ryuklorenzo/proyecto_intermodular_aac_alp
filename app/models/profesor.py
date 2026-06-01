from app.models.user import UserBase, UserOut

class ProfesorImport(UserBase):
    pass

class ProfesorOut(UserOut):
    id: int
    id_curso: int
    nivel: str
    curso: str
    modulo: str