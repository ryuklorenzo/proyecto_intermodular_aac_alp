from app.auth.auth import get_hash_password, TokenData, decode_token
from app.models.user import UserDb
from fastapi import status, HTTPException


db_config = {
    #"host": "127.0.0.1", # localhost si se prueba sin docker puerto 8082
    "host": "myapidb", # myapidb si se prueba desde docker puerto 8000
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

# usersAdmins : list[UserDb] = [
#     UserDb(id=1,
#         nombre="angel",
#         apellidos="angel",
#         activo=1,
#         password=get_hash_password("angel")),
#     UserDb(id=2,
#         nombre="azael",
#         apellidos="azael",
#         activo=1,
#         password=get_hash_password("azael"))
# ]

def validateIsAdmin(token) -> bool:
    # data: TokenData = decode_token(token)
    # if data.username not in [u.nombre for u in usersAdmins]:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Forbidden"
    #     )
    return True #Si se pone en false no tiran las funciones ver porque TODO