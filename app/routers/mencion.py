from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import mencion
from app.models.mencion import MencionImport, MencionOut
from app.auth.auth import oauth2_scheme
from app.database.mencion import (
    insert_mencion,
    read_all_menciones,
    read_mencion_by_id,
    read_menciones_by_reconocimiento,
    update_mencion,
    delete_mencion
)
from app.database.database_config import validateIsAdmin
from app.models.reconocimiento import ReconocimientoImport

router = APIRouter(
    prefix="/mentions",
    tags=["Mentions"]
)

@router.post("/recognitions/{id_reconocimiento}", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_mencion(
    mencion: MencionImport,
    id_reconocimiento: int,
):

    mencion_id = insert_mencion(id_reconocimiento, mencion)

    if mencion_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando mencion"
        )

    return {"message": "Mencion creado exitosamente", "id": mencion_id}



@router.get("/", response_model=List[MencionOut], status_code=status.HTTP_200_OK)
async def ver_reconocimientos(
    ):

    return read_all_menciones()


@router.get("/{id}", response_model=MencionOut, status_code=status.HTTP_200_OK)
async def ver_mencion_by_id(id: int):

    mencion = read_mencion_by_id(id)

    if not mencion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mencion no encontrado"
        )

    return mencion


@router.get("/recognitions/{id_reconocimiento}/", response_model=List[MencionOut], status_code=status.HTTP_200_OK)
async def ver_menciones_by_reconocimiento(id_reconocimiento: int):

    return read_menciones_by_reconocimiento(id_reconocimiento)


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_mencion(
    id:int,
    mencion: MencionImport,
    id_reconocimiento: int
):

    updated = update_mencion(id, mencion, id_reconocimiento)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Mencion no encontrada"
        )

    return {"message": "Mencion actualizada correctamente"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def borrar_mencion(
    id: int,
    ):

    deleted = delete_mencion(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mencion no encontrada"
        )

    return {"message": "Mencion eliminada correctamente"}