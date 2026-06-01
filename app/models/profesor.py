from app.models.user import UserOut

class ProfesorImport:
    pass

class ProfesorOut(UserOut):
    id: int
    id_curso: int
    nivel: str
    curso: str
    modulo: str