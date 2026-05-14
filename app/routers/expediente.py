from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models.expediente import ExpedienteImport, ExpedienteOut
from app.auth.auth import oauth2_scheme
from app.database.expediente import(
    insert_expediente, 
    read_all_expedientes, 
    read_expediente_by_directivo, 
)
from app.database.directivo import read_directivo_by_id
from app.database.database_config import validateIsAdmin


router = APIRouter(
    prefix="/records",
    tags=["Records"]
)

@router.post("/executives/{id_directivo}/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_expediente(id_directivo: int, expediente: ExpedienteImport, token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    usuario = read_directivo_by_id(id_directivo)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Directivo no encontrado")

    expediente_id = insert_expediente(id_directivo, expediente)
    if expediente_id == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar el expediente"
        )

    return {"message": "Expediente asignado correctamente", "id": expediente_id}


@router.get("/", response_model=List[ExpedienteOut], status_code=status.HTTP_200_OK)
async def ver_expedientes(token: str = Depends(oauth2_scheme)):
    if not validateIsAdmin(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )

    return read_all_expedientes()


@router.get("/executives/{id_directivo}/", response_model=List[ExpedienteOut], status_code=status.HTTP_200_OK)
async def ver_expedientes_por_directivo(id_directivo: int, token: str = Depends(oauth2_scheme)):
    
    expedientes = read_expediente_by_directivo(id_directivo)
    return expedientes