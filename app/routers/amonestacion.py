from app.auth.auth import oauth2_scheme # Si quieres proteger las rutas con token
from app.database.database_config import validateIsAdmin
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.actitud import  ActitudCreate
from app.models.amonestacion import AmonestacionBase, AmonestacionOut
from app.database.actitud import insert_actitud, delete_actitud
from app.database.amonestacion import (
    insert_amonestacion,
    read_all_amonestaciones,
    read_amonestacion_by_id,
    delete_amonestacion,
    read_amonestacion_by_userid
)

router = APIRouter(
    prefix="/reprimands",
    tags=["Reprimands"]
)

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def crear_amonestacion(
    id_alumno: int,
    id_profesor: int,
    amonestacion: AmonestacionBase,
    actitud: ActitudCreate,
    # token: str = Depends(oauth2_scheme)
):
    # if validateIsAdmin(token) == True:
        try:
            id_actitud = insert_actitud(id_alumno, actitud)
            id_amonestacion = insert_amonestacion(id_actitud, amonestacion, id_profesor)
            return {"message": "Amonestación asignada correctamente", "id": id_amonestacion}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la amonestación: {str(e)}"
            )
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="UNAUTHORIZED"

@router.get("/", response_model=List[AmonestacionOut], status_code=status.HTTP_200_OK)
async def ver_amonestaciones(
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    amonestaciones = read_all_amonestaciones()
    return amonestaciones

@router.get("/{id}", response_model=AmonestacionOut, status_code=status.HTTP_200_OK)
async def ver_amonestacion_por_id(
    id: int,
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    amonestacion = read_amonestacion_by_id(id)
    if not amonestacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Amonestación no encontrada")
    return amonestacion

@router.get("/students/{id_student}", response_model=List[AmonestacionOut]) 
async def ver_amonestaciones_de_alumno(
    id_alumno: int,
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    amonestacion = read_amonestacion_by_userid(id_alumno)
    if not amonestacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Amonestación no encontrada")
    return amonestacion