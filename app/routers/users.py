from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from app.core.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

from app.core.security import verify_api_key

@router.post("/", response_model=UserResponse, summary="Crear un nuevo usuario")
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    db_user = user_service.get_user_by_cedula(db, cedula=user.cedula)
    if db_user:
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[UserResponse], summary="Listar todos los usuarios")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{cedula}", response_model=UserResponse, summary="Obtener usuario por cédula")
def read_user(cedula: str, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_cedula(db, cedula=cedula)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user
