from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import ProfesorCreate, ProfesorDb
from app.auth.auth import oauth2_scheme # Si quieres proteger las rutas con token
from app.database import insert_profesor, read_all_profesores

router = APIRouter(
    prefix="/techers",
    tags=["Teachers"]
)

# 1. Insertar Profesors
@router.post("/teachers/create", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_profesor(profesor: ProfesorCreate):
    try: 
        profesor_id = insert_profesor(profesor)
        return {"message": "Profesor creado exitosamente", "id": profesor_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error"
        )


# 2. Ver todos los PROFESORES
@router.get("/", response_model=List[ProfesorDb], status_code=status.HTTP_200_OK)
async def read_all_profesores():
    # Aquí podrías añadir Depends(oauth2_scheme) si quieres que solo usuarios logueados lo vean
    profesores = read_all_profesores()
    return profesores