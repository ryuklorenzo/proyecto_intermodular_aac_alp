from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.actitud import ActitudCreate, ActitudOut
from app.auth.auth import oauth2_scheme
from app.database import (
    insert_actitud,
    read_actitudes_by_usuario,
    delete_actitud,
    read_user_by_id,
    validateIsAdmin
)

router = APIRouter(
    prefix="/attitudes",
    tags=["Attitudes"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_actitud(id_usuario: int, actitud: ActitudCreate, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    usuario = read_user_by_id(id_usuario)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    actitud_id = insert_actitud(id_usuario, actitud)
    if actitud_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar la actitud"
        )

    return {"message": "Actitud asignada correctamente", "id": actitud_id}


@router.get("/usuario/{id_usuario}/", response_model=List[ActitudOut], status_code=status.HTTP_200_OK)
async def ver_actitudes_alumno(id_usuario: int, token: str = Depends(oauth2_scheme)):
    
    actitudes = read_actitudes_by_usuario(id_usuario)
    return actitudes


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def borrar_actitud(id: int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    if not delete_actitud(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La actitud no existe"
        )

    return {"message": "Actitud eliminada correctamente"}