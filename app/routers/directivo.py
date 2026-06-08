from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import directivo
from app.models.directivo import DirectivoImport, DirectivoOut
from app.auth.auth import oauth2_scheme
from app.database.directivo import (
    insert_directivo,
    read_directivo_by_id,
    read_all_directivos,
    directivo_exists,
    baja_directivo
)
from app.auth.auth import validate_role

router = APIRouter(
    prefix="/executives",
    tags=["Executives"]
)

@router.post("/{id_profesor}/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_directivo(
    id_profesor: int,
    directivo: DirectivoImport,
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    if directivo_exists(id_profesor, directivo.cargo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Directivo con ese profesor y cargo ya existe"
        )
    directivo_id = insert_directivo(id_profesor, directivo)
    if directivo_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando el directivo"
        )
    return {"message": "Directivo creado exitosamente", "id": directivo_id}



@router.get("/", response_model=List[DirectivoOut], status_code=status.HTTP_200_OK)
async def ver_directivos(
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin", "directivo"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    directivos = read_all_directivos()
    return directivos


@router.get("/{id}/", response_model=DirectivoOut, status_code=status.HTTP_200_OK)
async def ver_directivo_por_id(
    id: int, 
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin", "directivo"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    directivo = read_directivo_by_id(id)
    if not directivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Directivo con id {id} no encontrado"
        )
    return directivo


@router.delete("/{id}/baja/", status_code=status.HTTP_200_OK)
async def dar_de_baja_directivo(id: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    directivo = read_directivo_by_id(id)
    if not directivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directivo no encontrado"
        )
    if not directivo.activo:
        return {"message": f"El directivo con id {id} ya estaba dado de baja previamente"}
    exito = baja_directivo(id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo dar de baja al Directivo (Error en BD)"
        )
    return {"message": f"Directivo con id {id} dado de baja correctamente (activo=False)"}
