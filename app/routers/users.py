from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Los datos de los usuarios se almacenan en la bsae de datos
class UserDb(BaseModel):
    id: int 
    name : str 
    username : str
    password : str
string
class UserIn(BaseModel):
    name : str 
    username : str
    password : str

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
@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(userIn : UserIn):
    userFound = [u for u in users if u.username == userIn.username and u.password == userIn.password]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password"
        )
    return userFound[0]

# Get all users
@router.get("/", status_code=status.HTTP_200_OK)
async def get_users():
    return users

# Get user by ID
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id : int):
    userFound = [u for u in users if u.id == id]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return userFound[0]

# Delete user by ID
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id : int):
    userFound = [u for u in users if u.id == id]
    if len(userFound) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    users.remove(userFound[0])
    return {"message": "User deleted successfully"}
