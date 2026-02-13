from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import ProfesorImport, ProfesorOut
from app.auth.auth import oauth2_scheme
from app.database import (
    insert_profesor,
    delete_profesor,
    read_all_profesores,
    read_profesor_by_id,
    profesor_exists,
    validateIsAdmin,
    baja_profesor
)

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_profesor(
    id_usuario: int,
    token: str = Depends(oauth2_scheme)
):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    if profesor_exists(id_usuario):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Profesor con ese usuario ya existe"
        )

    user_id = insert_user(asljd, sdajl, sdalj)
    profesor_id = insert_profesor(id_usuario)
    
    if profesor_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando el profesor"
        )

    return {"message": "Profesor creado exitosamente", "id": profesor_id}


@router.get("/", response_model=List[ProfesorOut], status_code=status.HTTP_200_OK)
async def ver_profesores(token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    profesores = read_all_profesores()
    return profesores


@router.get("/{id}/", response_model=ProfesorOut, status_code=status.HTTP_200_OK)
async def ver_profesor_por_id(id: int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    profesor = read_profesor_by_id(id)
    if not profesor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profesor con id {id} no encontrado"
        )
    return profesor


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
