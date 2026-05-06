from pydantic import BaseModel

class TokenOut(BaseModel):
    token: str

class UserLoginIn(BaseModel):
    nombre: str
    password: str

class TokenData(BaseModel):
    username: str
    role: str | None = None