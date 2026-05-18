from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.auth.auth import oauth2_scheme
from app.database.database_config import validateIsAdmin
from app.models.previ import PreviImport, PreviOut
from app.database.previ import (delete_previ, insert_previ, read_all_previes, read_previ_by_directivo, read_previ_by_expediente, update_previ)

router = APIRouter(
    prefix="/previ",
    tags=["Previ"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_previ(
    id_directivo: int,
    id_expediente: int,
    previ : PreviImport,
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para acceder a esta ruta.")
    
    # Aquí iría la lógica para obtener los datos de "previ" desde la base de datos
    previ_id = insert_previ(id_directivo, id_expediente, previ)
    if previ_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error al insertar el previ."
            )
    
    return {"message": "Previ insertado correctamente.", "id": previ_id}


@router.get("/expediente/{id_expediente}", response_model=List[PreviOut], status_code=status.HTTP_200_OK)
async def ver_previes_por_expediente(
    id_expediente: int, 
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para acceder a esta ruta.")
    
    # Aquí iría la lógica para obtener los datos de "previ" desde la base de datos
    return read_previ_by_expediente(id_expediente)


@router.get("/directivo/{id_directivo}", response_model=List[PreviOut], status_code=status.HTTP_200_OK)
async def ver_previes_por_directivo(
    id_directivo: int, 
    #TODO solo funciona al pasarle id expediente NOSE POR QUE
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para acceder a esta ruta.")
    
    # Aquí iría la lógica para obtener los datos de "previ" desde la base de datos
    return read_previ_by_directivo(id_directivo)


@router.get("/", response_model=List[PreviOut], status_code=status.HTTP_200_OK)
async def ver_todos_los_previes(
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para acceder a esta ruta.")
    
    # Aquí iría la lógica para obtener los datos de "previ" desde la base de datos
    return read_all_previes()


@router.put("/{id_previ}", status_code=status.HTTP_200_OK, response_model=dict)
async def actualizar_previ(
    id_previ: int, 
    previ: PreviImport, 
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para acceder a esta ruta.")
    
    # Aquí iría la lógica para actualizar los datos de "previ" en la base de datos
    updated = update_previ(id_previ, previ)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Previ no encontrado"
        )
    return {"message": "Previ actualizado correctamente."}


@router.delete("/{id_previ}", status_code=status.HTTP_200_OK, response_model=dict)
async def borrar_previ(
    id_previ: int, 
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para acceder a esta ruta.")
    
    # Aquí iría la lógica para eliminar el "previ" de la base de datos
    deleted = delete_previ(id_previ)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Previ no encontrado"
        )
    return {"message": "Previ eliminado correctamente."}