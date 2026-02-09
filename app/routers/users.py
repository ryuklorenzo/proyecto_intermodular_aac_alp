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
            nombre=userDb.nombre,
            apellidos=userDb.apellidos,
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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    # form de autenticacion
    username_input = form_data.username 
    password_input = form_data.password

    # busco en useradmins
    userFound = [u for u in usersAdmins if u.nombre == username_input] #Busque en root, o si tienen poderes ej directivo o profesor podian tener permisos
    
    if not userFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )
    # compruebo la contraseña
    user : UserDb = userFound[0]
    
    if not verify_password(plain_pw=password_input, hashed_pw=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )
    token = create_access_token(user)
    return token


# Get all users  ----------------------------------------(PEDIR TODOS LOS USUARIOS)-----------------------------------------------------------
@router.get("/",response_model=list[UserOut] ,status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        #coger los usuarios de la BD
        db_users = read_all_users()
        return [UserOut(id=u.id, nombre=u.nombre, apellidos=u.apellidos, activo=u.activo ) for u in db_users]
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
async def delete_user(UserDb : UserDb, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        deleted = deleteUser(UserDb)
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

