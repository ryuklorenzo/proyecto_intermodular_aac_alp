from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.models import UserBase, UserIn, UserDb, UserOut, UserLoginIn
from app.database import usersAdmins, insert_user, read_all_users, deleteUser, read_user_by_id
from app.auth.auth import create_access_token, verify_password, Token, oauth2_scheme, decode_token, TokenData, get_hash_password

#insertar alumno, ver alumnos, ver alumnoID, dar de baja

router = APIRouter(
    prefix="/alumnos",
    tags=["Alumnos"]
)

# User signup ----------------------------------------(CREAR USUARIO NUEVO)-----------------------------------------------------------
@router.post("/singup/", status_code=status.HTTP_201_CREATED)
async def create_user(userIn : UserIn):

    hashed_password = get_hash_password(userIn.password)
    new_user = UserDb(
        id=0, 
        name=userIn.name,
        username=userIn.username,
        password=hashed_password
    )
    try:
        user_id = insert_user(new_user)
        return {"message": "Usuario creado exitosamente", "id": user_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )







