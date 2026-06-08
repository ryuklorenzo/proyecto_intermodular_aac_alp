from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.database.curso import read_curso_by_id
from app.models.profesor import ProfesorImport, ProfesorOut
from app.auth.auth import oauth2_scheme
from app.database.profesor import (
    insert_profesor,
    read_all_profesores,
    read_profesor_by_id,
    profesor_exists,
    baja_profesor
)
from app.auth.auth import validate_role
from app.database.user import insert_user

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_profesor(
    id_curso: int,
    profesorBase : ProfesorImport, 
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    existe_curso = read_curso_by_id(id_curso)
    if not existe_curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso con id {id_curso} no encontrado"
        )

    user_id = insert_user(profesorBase)
    if profesor_exists(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Profesor con ese usuario ya existe"
        )
    profesor_id = insert_profesor(user_id, id_curso)
    if profesor_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando el profesor"
        )
    return {"message": "Profesor creado exitosamente", "id": profesor_id}


@router.get("/", response_model=List[ProfesorOut], status_code=status.HTTP_200_OK)
async def ver_profesores(token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo", 'profesor']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")

    profesores = read_all_profesores()
    return profesores


@router.get("/{id}/", response_model=ProfesorOut, status_code=status.HTTP_200_OK)
async def ver_profesor_por_id(id: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")

    profesor = read_profesor_by_id(id)
    if not profesor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profesor con id {id} no encontrado"
        )
    return profesor


@router.delete("/{id}/baja/", status_code=status.HTTP_200_OK)
async def dar_de_baja_profesor(id: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")

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
