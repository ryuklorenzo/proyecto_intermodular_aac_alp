from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import AlumnoCreate, AlumnoDb
from app.database import insert_alumno, read_all_alumnos, read_alumno_by_id, baja_alumno
from app.auth.auth import oauth2_scheme # Si quieres proteger las rutas con token

#insertar alumno, ver alumnos, ver alumnoID, dar de baja

router = APIRouter(
    prefix="/alumnos",
    tags=["Alumnos"]
)


# 1. Insertar Alumno
@router.post("/alumno_add/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_alumno(alumno: AlumnoCreate):
    try:
        # Nota: El id_usuario debe existir previamente en la tabla USUARIO
        alumno_id = insert_alumno(alumno)
        return {"message": "Alumno creado exitosamente", "id": alumno_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el alumno. Verifica que el id_usuario exista: {str(e)}"
        )


# 2. Ver todos los alumnos
@router.get("/", response_model=List[AlumnoDb], status_code=status.HTTP_200_OK)
async def ver_alumnos():
    # Aquí podrías añadir Depends(oauth2_scheme) si quieres que solo usuarios logueados lo vean
    alumnos = read_all_alumnos()
    return alumnos


# 3. Ver alumno por ID
@router.get("/{id}/", response_model=AlumnoCreate, status_code=status.HTTP_200_OK)
async def ver_alumno_por_id(id: int):
    alumno = read_alumno_by_id(id)
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con id {id} no encontrado"
        )
    return alumno


# 4. Dar de baja (Soft Delete)
@router.delete("/{id}/baja/", status_code=status.HTTP_200_OK)
async def dar_baja_alumno(id: int):
    # Primero verificamos si existe
    alumno = read_alumno_by_id(id)
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )
    
    # Procedemos a la baja
    exito = baja_alumno(id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo dar de baja al alumno"
        )
        
    return {"message": f"Alumno con id {id} dado de baja correctamente (activo=False)"}






