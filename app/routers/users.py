from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.models import UserBase, UserDb, UserOut, UserLoginIn
from app.database import usersAdmins, insert_user, read_all_users, deleteUser, read_user_by_id, validateIsAdmin
from app.auth.auth import create_access_token, verify_password, Token, oauth2_scheme, decode_token, TokenData, get_hash_password

'''
uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload
'''

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# User signup ----------------------------------------(CREAR USUARIO NUEVO)-----------------------------------------------------------
@router.post("/singup/", status_code=status.HTTP_201_CREATED)
async def create_user(userDb : UserDb, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        hashed_password = get_hash_password(userDb.password)
        new_user = UserDb(
            id=0, 
            name=userDb.nombre,
            username=userDb.apellidos,
            activo=userDb.activo,
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
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


# User login  ----------------------------------------(INICIAR SESION)-----------------------------------------------------------
@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()): # el depends asigna al form_data los datos que vienen en el body

    #1. Aqui compruebo que venga user y pwd en la peticion
    username: str | None = form_data.username
    password: str | None = form_data.password

    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )

    #2. Busco el usuario en la "base de datos"
    userFound = [u for u in usersAdmins if u.nombre == username]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )

    #3. Compruebo la contraseña
    user : UserDb = userFound[0]
    if not verify_password(plain_pw=password, hashed_pw=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )

    token = create_access_token(UserBase(username=user.nombre, password=user.password))
    return token


# Get all users  ----------------------------------------(PEDIR TODOS LOS USUARIOS)-----------------------------------------------------------
@router.get("/",response_model=list[UserOut] ,status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        #coger los usuarios de la BD
        db_users = read_all_users()
        return [UserOut(id=u.id, name=u.nombre, username=u.apellidos) for u in db_users]
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )
'''
payload
consta de tres partes:
"sub" : "luffy"          subject -> quien es el usuario
"iss": "PSP DAM"         issuer -> emisor del token
"exp" : 1918981595       expiration -> tiempo de expiracion del token

para la firma:
header.payload.signature
HMACSHA256(
    base64UrlEncode(header) + "." + base64UrlEncode(payload),
    secret
)
'''


# Get user by ID  ----------------------------------------(PEDIR UN USUARIO)-----------------------------------------------------------
@router.get("/{id}/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(id: int, token: str = Depends(oauth2_scheme)): 
    if validateIsAdmin(token) == True:
        # Buscamos en la base de datos usando la ID de la URL
        user_db = read_user_by_id(id)
        
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # Devolvemos el objeto, FastAPI se encarga de filtrarlo a UserOut
        return user_db
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


# Delete user by ID  ----------------------------------------(BORRAR USUARIO)-----------------------------------------------------------
@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def delete_user(userBase : UserBase, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        deleted = deleteUser(userBase)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, # O 404
                detail="Error: Usuario no encontrado o contraseña incorrecta"
            )
        return {"message": "Usuario eliminado correctamente"}
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )

