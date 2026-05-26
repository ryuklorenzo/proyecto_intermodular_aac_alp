from app.auth.auth import oauth2_scheme # Si quieres proteger las rutas con token
from app.database.database_config import validateIsAdmin
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.amonestacion import AmonestacionBase, AmonestacionOut
from app.database.actitud import insert_actitud, delete_actitud
from app.database.amonestacion import (
    insert_amonestacion,
    read_all_amonestaciones,
    read_amonestacion_by_id,
    delete_amonestacion
)

router = APIRouter(
    prefix="/reprimands",
    tags=["Reprimands"]
)

#TODO FURULA PERO DA ERROR POR TERMINAL EN API:  FIXXEAR
@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def crear_amonestacion(
    id_alumno: int,
    amonestacion: AmonestacionBase,
    # token: str = Depends(oauth2_scheme)
):
    # if validateIsAdmin(token) == True:
        try:
            id_actitud = insert_actitud(id_alumno, amonestacion)
            id_amonestacion = insert_amonestacion(id_actitud, amonestacion)
            return id_amonestacion

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la amonestación: {str(e)}"
            )
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="UNAUTHORIZED"
    #     )
#TODO para el out un AmonestacionOUT que llama diriectamente a actitud out y le añadimos el id de amonestacion