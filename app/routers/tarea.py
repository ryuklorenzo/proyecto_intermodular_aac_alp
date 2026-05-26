from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.tarea import TareaBase, TareaCreate, TareaOut
from app.auth.auth import oauth2_scheme
from app.database.tarea import (
    insert_tarea, 
    read_tareas_by_alumno, 
    read_tareas_by_profesor
)
from app.database.alumno import read_alumno_by_id
from app.database.profesor import read_profesor_by_id
from app.database.user import read_user_by_id
from app.database.database_config import validateIsAdmin

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_tarea(
    id_profesor: int,
    id_alumno: int,
    tarea: TareaBase,
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    if not read_alumno_by_id(id_alumno):
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    if not read_profesor_by_id(id_profesor):
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    new_tarea = TareaCreate(
        descripcion=tarea.descripcion,
        estado=tarea.estado,
        id_profesor=id_profesor,
        id_alumno=id_alumno
    )
    tarea_id = insert_tarea(new_tarea)

    if tarea_id == -1:
        raise HTTPException(status_code=500, detail="Error al crear la tarea")

    return {"message": "Tarea asignada correctamente", "id": tarea_id}

@router.get("/students/{id_alumno}/", response_model=List[TareaOut])
async def ver_tareas_alumno(
    id_alumno: int, 
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    tareas = read_tareas_by_alumno(id_alumno)
    return tareas


@router.get("/teachers/{id_profesor}/", response_model=List[TareaOut])
async def ver_tareas_profesor(
    id_profesor: int, 
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    tareas = read_tareas_by_profesor(id_profesor)
    return tareas