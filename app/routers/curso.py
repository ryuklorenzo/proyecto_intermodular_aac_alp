from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.curso import CursoCreate, CursoOut
from app.auth.auth import oauth2_scheme
from app.database.curso import (
    insert_curso,
    read_all_cursos,
    read_curso_by_id,
    update_curso,
    delete_curso,
)
from app.database.database_config import validateIsAdmin

router = APIRouter(
    prefix="/cursos",
    tags=["Cursos"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_curso(
    curso: CursoCreate,
    token: str = Depends(oauth2_scheme)
):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    curso_id = insert_curso(curso)

    if curso_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando curso"
        )

    return {"message": "Curso creado exitosamente", "id": curso_id}



@router.get("/", response_model=List[CursoOut], status_code=status.HTTP_200_OK)
async def ver_directivos(token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    return read_all_cursos()


@router.get("/{id}/", response_model=CursoOut, status_code=status.HTTP_200_OK)
async def ver_curso_by_id(id:int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )

    curso = read_curso_by_id(id)

    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")

    return curso


@router.put("/{id}/", status_code=status.HTTP_200_OK)
async def actualizar_curso(
    id:int,
    curso: CursoCreate,
    token: str = Depends(oauth2_scheme)
):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    updated = update_curso(id, curso)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    return {"message": "Curso actualizado correctamente"}


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def borrar_curso(id: int, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    deleted = delete_curso(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )

    return {"message": "Curso eliminado correctamente"}