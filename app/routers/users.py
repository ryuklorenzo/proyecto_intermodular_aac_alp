from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.models import UserBase, UserIn, UserDb, UserOut, UserLoginIn
from app.database import users
from app.auth.auth import create_access_token, verify_password, Token

'''
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
'''

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# User signup ----------------------------------------(CREAR USUARIO NUEVO)-----------------------------------------------------------
@router.post("/singup/", status_code=status.HTTP_201_CREATED)
async def create_user(userIn : UserIn):
    userFound = [u for u in users if u.username == userIn.username]
    if len(userFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That username already exists"
        )

    users.append(
        UserDb(
            id = len(users) + 1,
            name = userIn.name,
            username = userIn.username,
            password = userIn.password
        )
    )

# User login  ----------------------------------------(INICIAR SESION)-----------------------------------------------------------
@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()): # el depends asigna al form_data los datos que vienen en el body
    
    #aqui compruebo que venga user y pwd en la peticion
    username: str | None = form_data.get("username")
    password: str | None = form_data.get("password")
    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )
    
    #Busco el usuario en la "base de datos"
    userFound = [u for u in users if u.username == username]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )
    
    #Compruebo la contraseña
    user : UserDb = userFound[0]
    if verify_password(plain_pw=password, hashed_pw=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )
    
    token = create_access_token(UserBase(username=user.username, password=user.password))
    return token


# Get all users  ----------------------------------------(PEDIR TODOS LOS USUARIOS)-----------------------------------------------------------
@router.get("/",response_model=list[UserOut] ,status_code=status.HTTP_200_OK)
async def get_all_users(authorization: str | None = Header()):
    print(authorization)
    
    parts = authorization.split(":") #asi separamos mytoken de lo demas
    if len(parts) !=2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    if parts[0] != "mytoken": #verificamos que el token sea correcto
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    paylaod_parts = parts[1].split("--")
    if len(paylaod_parts) !=2: #asi separamos username de name
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    username = paylaod_parts[0]
    if username not in [u.username for u in users] :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    return [UserOut(id=UserDb.id, name=UserDb.name, username=UserDb.username) for UserDb in users]
    #tecnicamente es lo mismo que: "return users" ya que FastAPI se encarga de hacer el filtrado poniendole el response_model
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
async def delete_user(userDb : UserDb):
    userFound = [u for u in users if u.id == userDb.id]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    users.remove(userFound[0])
    return {"message": "User deleted successfully"}
