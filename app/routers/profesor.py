from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import ProfesorCreate, ProfesorDb
from app.auth.auth import oauth2_scheme, TokenData # Si quieres proteger las rutas con token
from app.database import insert_profesor, read_all_profesores, profesor_exists, validateIsAdmin

router = APIRouter(
    prefix="/techers",
    tags=["Teachers"]
)

# 1. Insertar Profesors
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_profesor(profesor: ProfesorCreate, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        try: 
            if profesor_exists(profesor.nombre, profesor.apellidos) == False:
                profesor_id = insert_profesor(profesor)
                return {"message": "Profesor creado exitosamente", "id": profesor_id}
            else: 
                raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error, ese profesor ya esta creado"
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"UNAUTHORIZED"
            )


# 2. Ver todos los PROFESORES
@router.get("/", response_model=List[ProfesorDb], status_code=status.HTTP_200_OK)
async def ver_profesores(token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
    # Aquí podrías añadir Depends(oauth2_scheme) si quieres que solo usuarios logueados lo vean 
        profesores = read_all_profesores()
        return profesores
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )