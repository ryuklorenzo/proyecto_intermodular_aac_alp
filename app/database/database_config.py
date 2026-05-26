from app.auth.auth import get_hash_password, TokenData, decode_token
from app.models.user import UserDb
from fastapi import status, HTTPException

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

usersAdmins : list[UserDb] = [
    UserDb(id=1,
        nombre="angel",
        apellidos="angel",
        activo=1,
        password=get_hash_password("angel")),
    UserDb(id=2,
        nombre="azael",
        apellidos="azael",
        activo=1,
        password=get_hash_password("azael"))
]

def validateIsAdmin(token) -> bool:
    data: TokenData = decode_token(token)
    if data.username not in [u.nombre for u in usersAdmins]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return True