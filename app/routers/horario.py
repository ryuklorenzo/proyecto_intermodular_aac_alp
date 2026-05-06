from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.horario import HorarioImport, HorarioOut
from app.auth.auth import oauth2_scheme
from app.database import (
    insert_horario,
    read_all_horarios,
    update_horario,
    delete_horario,
    validateIsAdmin
)

router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_horario(
    horario: HorarioImport,
    token: str = Depends(oauth2_scheme)
):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    horario_id = insert_horario(horario)

    if horario_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando horario"
        )

    return {"message": "Horario creado exitosamente", "id": horario_id}



@router.get("/", response_model=List[HorarioOut], status_code=status.HTTP_200_OK)
async def ver_directivos(token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    return read_all_horarios()


@router.put("/{id}/", status_code=status.HTTP_200_OK)
async def actualizar_horario(
    id:int,
    horario: HorarioImport,
    token: str = Depends(oauth2_scheme)
):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    updated = update_horario(id, horario)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )

    return {"message": "Horario actualizado correctamente"}


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def borrar_directivo(id: int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    deleted = delete_horario(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )

    return {"message": "Horario eliminado correctamente"}