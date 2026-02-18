from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import AlumnoCreate, AlumnoOut
from app.database import (
    insert_alumno, 
    read_all_alumnos, 
    read_alumno_by_id, 
    baja_alumno, 
    validateIsAdmin,
    insert_user
)
from app.auth.auth import oauth2_scheme # Si quieres proteger las rutas con token

#insertar alumno, ver alumnos, ver alumnoID, dar de baja

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# 1. Insertar Alumno
@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_alumno(alumno: AlumnoCreate, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        try:
            # Nota: El id_usuario debe existir previamente en la tabla USUARIO
            user_id = insert_user(alumno)
            alumno_id = insert_alumno(user_id, alumno)
            return {"message": "Alumno creado exitosamente", "id": user_id}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el alumno. Verifica que el id_usuario exista: {str(e)}"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )



# 2. Ver todos los alumnos
@router.get("/", response_model=List[AlumnoOut], status_code=status.HTTP_200_OK)
async def ver_alumnos(token: str = Depends(oauth2_scheme)):
    # Aquí podrías añadir Depends(oauth2_scheme) si quieres que solo usuarios logueados lo vean
    if validateIsAdmin(token) == True:
        alumnos = read_all_alumnos()
        return alumnos
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )

# 3. Ver alumno por ID
@router.get("/{id}/", response_model=AlumnoOut, status_code=status.HTTP_200_OK)
async def ver_alumno_por_id(id: int, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        alumno = read_alumno_by_id(id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alumno con id {id} no encontrado"
            )
        return alumno
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


# 4. Dar de baja (Soft Delete)
@router.delete("/{id}/baja/", status_code=status.HTTP_200_OK)
async def dar_baja_alumno(id: int, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
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
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )






