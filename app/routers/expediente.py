from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.expediente import ExpedienteImport, ExpedienteOut
from app.auth.auth import oauth2_scheme
from app.database.expediente import(
    insert_expediente, 
    read_all_expedientes,
    read_expediente_by_alumno, 
    read_expediente_by_directivo, 
)
from app.database.directivo import read_directivo_by_id
from app.auth.auth import validate_role

router = APIRouter(
    prefix="/records",
    tags=["Records"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_expediente(id_directivo: int, id_alumno: int, expediente: ExpedienteImport, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    
    usuario = read_directivo_by_id(id_directivo)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directivo no encontrado")
    
    expediente_id = insert_expediente(id_alumno, id_directivo, expediente)
    if expediente_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar el expediente"
        )

    return {"message": "Expediente asignado correctamente", "id": expediente_id}


@router.get("/", response_model=List[ExpedienteOut], status_code=status.HTTP_200_OK)
async def ver_expedientes(token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    return read_all_expedientes()


@router.get("/executives/{id_directivo}/", response_model=List[ExpedienteOut], status_code=status.HTTP_200_OK)
async def ver_expedientes_por_directivo(id_directivo: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    expedientes = read_expediente_by_directivo(id_directivo)
    return expedientes


@router.get("/students/{id_alumno}/", response_model=List[ExpedienteOut], status_code=status.HTTP_200_OK)
async def ver_expedientes_por_alumno(id_alumno: int, token: str = Depends(oauth2_scheme)):
    if not validate_role(token, ["admin", "directivo"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permisos")
    
    expedientes = read_expediente_by_alumno(id_alumno)
    return expedientes