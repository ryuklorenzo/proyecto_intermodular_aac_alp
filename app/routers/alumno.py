from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.database.curso import read_curso_by_id
from app.models.alumno import AlumnoCreate, AlumnoOut
from app.auth.auth import oauth2_scheme 
from app.database.user import insert_user
from app.database.alumno import (
    insert_alumno, 
    read_all_alumnos, 
    read_alumno_by_id, 
    baja_alumno, 
)
from app.auth.auth import validate_role


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# Insertar Alumno
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_alumno(
    id_curso: int,
    alumno: AlumnoCreate, 
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    try:
        existe_curso = read_curso_by_id(id_curso)
        if not existe_curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso con id {id_curso} no encontrado"
            )
        user_id = insert_user(alumno)
        alumno_id = insert_alumno(user_id, id_curso)
        return {"message": "Alumno creado exitosamente", "id": user_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el alumno. Verifica que el id_usuario exista: {str(e)}"
        )


# Ver todos los alumnos
@router.get("/", response_model=List[AlumnoOut], status_code=status.HTTP_200_OK)
async def ver_alumnos(token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
        
    else:
        alumnos = read_all_alumnos()
        return alumnos


# Ver alumno por ID
@router.get("/{id}/", response_model=AlumnoOut, status_code=status.HTTP_200_OK)
async def ver_alumno_por_id(id: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    alumno = read_alumno_by_id(id)
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con id {id} no encontrado"
        )
    return alumno


# Dar de baja alumno (activo=False)
@router.delete("/{id}/baja/", status_code=status.HTTP_200_OK)
async def dar_baja_alumno(id: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    
    alumno = read_alumno_by_id(id)
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
            )
        
    if not alumno.activo:
        return {"message": f"El alumno con id {id} ya estaba dado de baja previamente"}

    exito = baja_alumno(id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo dar de baja al alumno (Error en BD)"
        )
        
    return {"message": f"Alumno con id {id} dado de baja correctamente (activo=False)"}
