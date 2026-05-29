from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.aula_convivencia import AulaConvivenciaImport, AulaConvivenciaOut
from app.models.aula_convivencia_alumno import AulaConvivenciaAlumnoImport, AulaConvivenciaAlumnoOut
from app.auth.auth import oauth2_scheme
from app.database.aula_convivencia import (
    assign_alumnos_to_aula,
    insert_aula_convivencia,
    read_all_aulas_convivencia,
    read_alumnos_in_aula,
    read_aula_convivencia_by_id,
    remove_alumno_from_aula,
    update_aula_convivencia,
    delete_aula_convivencia
)
from app.database.database_config import validateIsAdmin

router = APIRouter(
    prefix="/aula_convivencia",
    tags=["Aula_Convivencia"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_aula_convivencia(
    aula: AulaConvivenciaImport,
    id_horario: int,
):

    aula_id = insert_aula_convivencia(id_horario, aula)

    if aula_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando aula de convivencia"
        )

    return {"message": "Aula de convivencia creado exitosamente", "id": aula_id}


@router.get("/", response_model=List[AulaConvivenciaOut], status_code=status.HTTP_200_OK)
async def ver_aulas_convivencia(
    ):

    return read_all_aulas_convivencia()


@router.get("/{id}", response_model=AulaConvivenciaOut, status_code=status.HTTP_200_OK)
async def ver_aula_convivencia_by_id(id: int):

    aula = read_aula_convivencia_by_id(id)

    if not aula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula de convivencia no encontrada"
        )

    return aula


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_aula_convivencia(
    id:int,
    aula: AulaConvivenciaImport,
    id_horario: int
):

    updated = update_aula_convivencia(id, aula, id_horario)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Aula de convivencia no encontrada"
        )

    return {"message": "Aula de convivencia actualizado correctamente"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def borrar_aula_convivencia(
    id: int,
    ):

    deleted = delete_aula_convivencia(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula de convivencia no encontrada"
        )

    return {"message": "Aula de convivencia eliminado correctamente"}


@router.post("/assign-students", status_code=status.HTTP_200_OK)
async def asignar_alumnos_aula(
    data: AulaConvivenciaAlumnoImport
):

    assigned = assign_alumnos_to_aula(
        data.id_aula_convivencia,
        data.alumnos_ids
    )

    if not assigned:
        raise HTTPException(
            status_code=404,
            detail="Error asignando alumnos"
        )

    return {"message": "Alumnos asignados correctamente"}


@router.get("/{id_aula}/students", response_model=List[AulaConvivenciaAlumnoOut], status_code=status.HTTP_200_OK)
async def ver_alumnos_en_aula(
    id_aula: int, 
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    aula = read_aula_convivencia_by_id(id_aula)
    if not aula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula de convivencia no encontrada"
        )
        
    return read_alumnos_in_aula(id_aula)


@router.delete("/{id_aula}/students/{id_alumno}", status_code=status.HTTP_200_OK)
async def sacar_alumno_de_aula(
    id_aula: int, 
    id_alumno: int, 
    # token: str = Depends(oauth2_scheme)
):
    # if not validateIsAdmin(token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    aula = read_aula_convivencia_by_id(id_aula)
    if not aula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula de convivencia no encontrada"
        )

    exito = remove_alumno_from_aula(id_aula, id_alumno)
    
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El alumno no se encuentra en esta aula de convivencia o no se pudo sacar"
        )

    return {"message": "Alumno sacado del aula de convivencia correctamente"}