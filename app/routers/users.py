from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.models import UserBase, UserIn, UserDb, UserOut, UserLoginIn
from app.database import usersAdmins, insert_user, read_all_users, deleteUser
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
    userFound = [u for u in usersAdmins if u.username == username]
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

    token = create_access_token(UserBase(username=user.username, password=user.password))
    return token


# Get all users  ----------------------------------------(PEDIR TODOS LOS USUARIOS)-----------------------------------------------------------
@router.get("/",response_model=list[UserOut] ,status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(oauth2_scheme)):

    data : TokenData = decode_token(token)
    #verificamos que sea un usuario con poderes
    if data.username not in [u.username for u in usersAdmins] :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    #coger los usuarios de la BD
    db_users = read_all_users()
    return [UserOut(id=u.id, name=u.name, username=u.username) for u in db_users]

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
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(userDb : UserDb):
    userFound = [u for u in users if u.id == userDb.id]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return userFound[0]

# Delete user by ID  ----------------------------------------(BORRAR USUARIO)-----------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(userBase : UserBase):
    
    db_users = read_all_users()
    userFound = [u for u in db_users if u.username == userBase.username]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )    
    return deleteUser(userFound[0])
