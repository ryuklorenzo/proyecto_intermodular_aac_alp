from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import TareaCreate, TareaOut
from app.auth.auth import oauth2_scheme
from app.database import (
    insert_tarea,
    read_tareas_by_alumno,
    read_tareas_by_profesor,
    read_user_by_id,
    validateIsAdmin
)

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"]
)

@router.post("/create/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_tarea(tarea: TareaCreate, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    tarea_id = insert_tarea(tarea)

    if tarea_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la tarea"
        )

    return {"message": "Tarea asignada correctamente", "id": tarea_id}


@router.get("/alumno/{id_alumno}/", response_model=List[TareaOut])
async def ver_tareas_alumno(id_alumno: int, token: str = Depends(oauth2_scheme)):
    
    tareas = read_tareas_by_alumno(id_alumno)
    return tareas


@router.get("/alumno/{id_profesor}/", response_model=List[TareaOut])
async def ver_tareas_profesor(id_profesor: int, token: str = Depends(oauth2_scheme)):
    
    tareas = read_tareas_by_profesor(id_profesor)
    return tareas