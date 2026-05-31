from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.probi import ProbiImport, ProbiOut
from app.auth.auth import oauth2_scheme
from app.database.probi import (
    insert_probi,
    read_all_probis,
    read_probi_by_id,
    update_probi,
    delete_probi
)
from app.auth.auth import validate_role

router = APIRouter(
    prefix="/probis",
    tags=["Probi"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_probi(
    aula: ProbiImport,
    id_mencion: int,
):

    probi_id = insert_probi(id_mencion, aula)

    if probi_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando probi"
        )

    return {"message": "Probi creado exitosamente", "id": probi_id}



@router.get("/", response_model=List[ProbiOut], status_code=status.HTTP_200_OK)
async def ver_probi(
    ):

    return read_all_probis()


@router.get("/{id}", response_model=ProbiOut, status_code=status.HTTP_200_OK)
async def ver_probi_by_id(id: int):

    probi = read_probi_by_id(id)

    if not probi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Probi no encontrada"
        )

    return probi


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_probi(
    id:int,
    probi: ProbiImport,
    id_mencion: int
):

    updated = update_probi(id, probi, id_mencion)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Probi no encontrada"
        )

    return {"message": "Probi actualizado correctamente"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def borrar_probi(
    id: int,
    ):

    deleted = delete_probi(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Probi no encontrada"
        )

    return {"message": "Probi eliminado correctamente"}