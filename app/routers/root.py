from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.models import UserBase, UserIn, UserDb, UserOut, UserLoginIn
from app.database import usersAdmins, insert_user, read_all_users, deleteUser, read_user_by_id
from app.auth.auth import create_access_token, verify_password, Token, oauth2_scheme, decode_token, TokenData, get_hash_password

# insertar root, borrar root, ver roots

router = APIRouter(
    prefix="/roots",
    tags=["Roots"]
)