from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.models import DirectivoCreate, DirectivoDb, DirectivoBase
from app.auth.auth import oauth2_scheme, TokenData # Si quieres proteger las rutas con token
from app.database import insert_directivo, read_directivo_by_id, read_all_directivos, directivo_exists, validateIsAdmin, delete_directivo as delete_directivo_db

router = APIRouter(
    prefix="/executives",
    tags=["Executives"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict)
async def crear_directivo(directivo: DirectivoCreate, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        try: 
            if directivo_exists(directivo.nombre, directivo.apellidos, directivo.cargo) == False:
                directivo_id = insert_directivo(directivo) #FALTA AÑADIR EL ID-USUARIO
                return {"message": "directivo creado exitosamente", "id": directivo_id}
            else: 
                raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error, ese directivo ya esta creado"
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"UNAUTHORIZED"
            )


@router.get("/", response_model=List[DirectivoDb], status_code=status.HTTP_200_OK)
async def ver_directivo(token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
    # Aquí podrías añadir Depends(oauth2_scheme) si quieres que solo usuarios logueados lo vean 
        directivo = read_all_directivos()
        return directivo
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


@router.get("/{id}/", response_model=DirectivoCreate, status_code=status.HTTP_200_OK)
async def ver_directivo_por_id(id: int, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        directivo = read_directivo_by_id(id)
        if not directivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Directivo con id {id} no encontrado"
            )
        return directivo
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def delete_directivo(id: int, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        deleted = delete_directivo_db(id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, # O 404
                detail="Error: Directivo no encontrado"
            )
        return {"message": "Directivo eliminado correctamente"}
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )