from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserBase, UserDb, UserOut
from app.database.user import (
    get_user_for_login,
    insert_user,
    read_all_users, 
    deleteUser, 
    read_user_by_id
)
from app.auth.auth import (
    create_access_token, 
    verify_password, 
    Token, oauth2_scheme, 
    get_hash_password
    )

'''
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload
'''

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# User signup ----------------------------------------(CREAR USUARIO NUEVO)-----------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    userbase : UserBase, 
    token: str = Depends(oauth2_scheme)
):
    try:
        hashed_password = get_hash_password(userbase.password)
        new_user = UserBase(
            nombre=userbase.nombre,
            apellidos=userbase.apellidos,
            activo=userbase.activo,
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
    except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


# User login  ----------------------------------------(INICIAR SESION)-----------------------------------------------------------
@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user_db = get_user_for_login(form_data.username)
    
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    #comprobar si está activo
    if not user_db["activo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está desactivado"
        )

    if not verify_password(plain_pw=form_data.password, hashed_pw=user_db["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {
        "sub": str(user_db["id"]), #guardamos el ID en el subject
        "role": user_db["rol"]     #inyectamos el rol
    }
    access_token = create_access_token(data=token_data)

    #Devuelve el token y el rol según el response_model
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user_db["rol"]
    }


# Get all users  ----------------------------------------(PEDIR TODOS LOS USUARIOS)-----------------------------------------------------------
@router.get("/",response_model=list[UserOut] ,status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(oauth2_scheme)):
    try:
        #coger los usuarios de la BD
        db_users = read_all_users()
        return [UserOut(id=u.id, nombre=u.nombre, apellidos=u.apellidos, activo=u.activo ) for u in db_users]
    except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


# Get user by ID  ----------------------------------------(PEDIR UN USUARIO)-----------------------------------------------------------
@router.get("/{id}/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(id: int, token: str = Depends(oauth2_scheme)): 
    try:
        # Buscamos en la base de datos usando la ID de la URL
        user_db = read_user_by_id(id)
        
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # Devolvemos el objeto, FastAPI se encarga de filtrarlo a UserOut
        return user_db
    except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


# Delete user by ID  ----------------------------------------(BORRAR USUARIO)-----------------------------------------------------------
@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def delete_user(UserDb : UserDb, token: str = Depends(oauth2_scheme)):
    try:
        deleted = deleteUser(UserDb)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, # O 404
                detail="Error: Usuario no encontrado o contraseña incorrecta"
            )
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )

