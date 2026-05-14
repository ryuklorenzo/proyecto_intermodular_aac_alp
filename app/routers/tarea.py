from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.tarea import TareaCreate, TareaOut
from app.auth.auth import oauth2_scheme
from app.database.tarea import (
    insert_tarea, 
    read_tareas_by_alumno, 
    read_tareas_by_profesor
)
from app.database.user import read_user_by_id
from app.database.database_config import validateIsAdmin

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_tarea(
    tarea: TareaCreate,
    token: str = Depends(oauth2_scheme)
):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    new_tarea = TareaCreate(
        descripcion=tarea.descripcion,
        estado=tarea.estado,
        id_profesor=tarea.id_profesor,
        id_alumno=tarea.id_alumno
    )
    tarea_id = insert_tarea(tarea)

    if tarea_id == -1:
        raise HTTPException(status_code=500, detail="Error al crear la tarea")

    return {"message": "Tarea asignada correctamente", "id": tarea_id}

@router.get("/students/{id_alumno}/", response_model=List[TareaOut])
async def ver_tareas_alumno(id_alumno: int, token: str = Depends(oauth2_scheme)):
    
    tareas = read_tareas_by_alumno(id_alumno)
    return tareas


@router.get("/teachers/{id_profesor}/", response_model=List[TareaOut])
async def ver_tareas_profesor(id_profesor: int, token: str = Depends(oauth2_scheme)):
    
    tareas = read_tareas_by_profesor(id_profesor)
    return tareas