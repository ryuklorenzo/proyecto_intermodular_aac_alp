from fastapi import HTTPException, status
import bcrypt

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

from app.models.user import UserBase

SECRET_KEY = "1234567890" #3f5a2fc8da7cfef74c16ec6b3da25cc401052930c0b4979c1bedb664168fc486
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 7 * 24 * 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

db_config = {
    #"host": "127.0.0.1", # localhost si se prueba sin docker puerto 8082
    "host": "myapidb", # myapidb si se prueba desde docker puerto 8000
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str 


class TokenData(BaseModel):
    username: str | None = None


def get_hash_password(plain_pw: str) -> str:
    pw_bytes = plain_pw.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password=pw_bytes, salt=salt)
    return hashed_pw


def verify_password(plain_pw, hashed_pw) -> bool:
    plain_pw_bytes = plain_pw.encode("utf-8")
    hashed_pw_bytes = hashed_pw.encode("utf-8")
    return bcrypt.checkpw(password=plain_pw_bytes, hashed_password=hashed_pw_bytes)


def create_access_token(data: dict) -> str:
    #copia por si hay error
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    #añadimos la expiración al diccionario 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(username=payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

def validate_role(token: str, allowed_roles: list[str]) -> bool:
    """
    Comprueba si el rol guardado en el token está dentro de la lista de roles permitidos.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        
        # Comprobamos si el rol del usuario está en la lista de permitidos
        return role in allowed_roles
        
    except Exception as e:
        print(f"Error validando token: {e}")
        return False