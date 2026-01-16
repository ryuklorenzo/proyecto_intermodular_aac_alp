'''from os import read
from fastapi import APIRouter, Depends, status, HTTPException
from app.models import RootIn, RootDb, RootOut
from app.database import usersAdmins, read_all_roots, delete_root, insert_root, validateIsAdmin
from app.auth.auth import  oauth2_scheme, decode_token, TokenData

# insertar root, borrar root, ver roots

router = APIRouter(
    prefix="/roots",
    tags=["Roots"]
)

#----------------------------------------(CREAR ROOT NUEVO)-----------------------------------------------------------
@router.post("/root_add/", status_code=status.HTTP_201_CREATED)
async def create_root(rootIn : RootIn, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        new_root = RootDb(id=0, name=rootIn.name, code=rootIn.code)
        
        try:
            root_id = insert_root(new_root)
            return {"message": "Root creado exitosamente", "id": root_id}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el root: {str(e)}"
        )
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"UNAUTHORIZED"
            )
    

#----------------------------------------(OBTENER TODOS LOS ROOTS)-----------------------------------------------------------
@router.get("/", response_model=list[RootOut], status_code=status.HTTP_200_OK)
async def get_all_roots(token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        return read_all_roots()
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"UNAUTHORIZED"
            )
    


# Delete ROOT ----------------------------------------(BORRAR ROOT)-----------------------------------------------------------
@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def delete_root_e(id: int, token: str = Depends(oauth2_scheme)):
    if validateIsAdmin(token) == True:
        deleted = delete_root(id)

        if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Root not found"
                )
        return {"message": "Root eliminado correctamente"}
    else:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"UNAUTHORIZED"
                )
'''