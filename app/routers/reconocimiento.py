from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.database.actitud import insert_actitud
from app.models.actitud import ActitudCreate
from app.models.reconocimiento import ReconocimientoImport, ReconocimientoOut
from app.auth.auth import oauth2_scheme
from app.database.reconocimiento import (
    insert_reconocimiento,
    read_all_reconocimientos,
    read_reconocimiento_by_id,
    read_reconocimientos_by_actitud,
    update_reconocimiento,
    delete_reconocimiento
)
from app.auth.auth import validate_role

router = APIRouter(
    prefix="/recognitions",
    tags=["Recognitions"]
)

@router.post("/attitudes/{id_actitud}", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_reconocimiento(
    id_alumno: int,
    id_profesor: int,
    reconocimiento: ReconocimientoImport,
    actitud: ActitudCreate,
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")

    id_actitud = insert_actitud(id_alumno, actitud)
    reconocimiento_id = insert_reconocimiento(id_actitud, reconocimiento, id_profesor)
    if reconocimiento_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando reconocimiento"
        )
    return {"message": "Reconocimiento creado exitosamente", "id": reconocimiento_id}



@router.get("/", response_model=List[ReconocimientoOut], status_code=status.HTTP_200_OK)
async def ver_reconocimientos(
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")

    return read_all_reconocimientos()


@router.get("/{id}", response_model=ReconocimientoOut, status_code=status.HTTP_200_OK)
async def ver_reconocimiento_by_id(id: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    reconocimiento = read_reconocimiento_by_id(id)

    if not reconocimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reconocimiento no encontrado"
        )

    return reconocimiento


@router.get("/attitudes/{id_actitud}/", response_model=List[ReconocimientoOut], status_code=status.HTTP_200_OK)
async def ver_reconocimientos_by_actitud(id_actitud: int, token: str = Depends(oauth2_scheme)):

    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")

    return read_reconocimientos_by_actitud(id_actitud)


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_reconocimiento(
    id:int,
    reconocimiento: ReconocimientoImport,
    id_actitud: int,
    token: str = Depends(oauth2_scheme)
):
    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    updated = update_reconocimiento(id, reconocimiento, id_actitud)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Reconocimiento no encontrado"
        )

    return {"message": "Reconocimiento actualizado correctamente"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def borrar_reconocimiento(id: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo", "profesor"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    deleted, mensaje = delete_reconocimiento(id)
    if not deleted:
        if mensaje == "not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reconocimiento no encontrado"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se puede borrar el reconocimiento porque tiene una mención asociada. Error DB: {mensaje}"
            )
    return {"message": "Reconocimiento eliminado correctamente"}