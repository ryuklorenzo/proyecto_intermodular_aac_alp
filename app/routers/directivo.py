from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import DirectivoImport, DirectivoOut
from app.auth.auth import oauth2_scheme
from app.database import (
    insert_directivo,
    read_directivo_by_id,
    read_all_directivos,
    directivo_exists,
    validateIsAdmin,
    delete_directivo as delete_directivo_db
)

router = APIRouter(
    prefix="/executives",
    tags=["Executives"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_directivo(directivo: DirectivoImport, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

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
async def ver_directivos(token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    directivos = read_all_directivos()
    return directivos


@router.get("/{id}/", response_model=DirectivoOut, status_code=status.HTTP_200_OK)
async def ver_directivo_por_id(id: int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    directivo = read_directivo_by_id(id)
    if not directivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Directivo con id {id} no encontrado"
        )
    return directivo


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def borrar_directivo(id: int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    deleted = delete_directivo_db(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directivo no encontrado"
        )

    return {"message": "Directivo eliminado correctamente"}


'''
@router.delete("/{id}/baja/", status_code=status.HTTP_200_OK)
async def dar_de_baja_profesor(id: int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    profesor = read_profesor_by_id(id)
    if not profesor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    
    if not profesor.activo:
        return {"message": f"El profesor con id {id} ya estaba dado de baja previamente"}
    
    exito = baja_profesor(id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo dar de baja al Profesor (Error en BD)"
        )
        
    return {"message": f"Profesor con id {id} dado de baja correctamente (activo=False)"}
'''