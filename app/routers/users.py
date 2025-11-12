from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#Usuario base
class UserBase(BaseModel):
    username : str
    password : str

class UserIn(UserBase):
    name : str 

# Los datos de los usuarios se almacenan en la bsae de datos
class UserDb(UserIn):
    id: int 

# Formato de respuesta al iniciar sesión
class TokenOut(BaseModel):
    token: str

class UserLoginIn(UserBase):
    pass


users : list[UserDb] = []

# User signup
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

# User login
@router.post("/login/", response_model=TokenOut, status_code=status.HTTP_200_OK)
async def login(userLoginIn : UserLoginIn):
    userFound = [u for u in users if u.username == userLoginIn.username]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )
    
    user : UserDb = userFound[0]
    if user.password != userLoginIn.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and/or password"
        )
    
    return TokenOut(
        token=f"mytoken:{user.username}--{user.name}"
        )

# Get all users
@router.get("/", status_code=status.HTTP_200_OK)
async def get_users():
    return users

# Get user by ID
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(userDb : UserDb):
    userFound = [u for u in users if u.id == userDb.id]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return userFound[0]

# Delete user by ID
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
