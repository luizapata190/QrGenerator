from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
import logging

logger = logging.getLogger(__name__)

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_cedula(db: Session, cedula: str):
    logger.debug(f"Searching user by cedula", extra={"cedula": cedula})
    return db.query(User).filter(User.cedula == cedula).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    logger.debug(f"Listing users", extra={"skip": skip, "limit": limit})
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    logger.info(f"Creating new user", extra={"cedula": user.cedula, "email": user.email})
    db_user = User(cedula=user.cedula, nombre=user.nombre, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created successfully", extra={"user_id": db_user.id})
    return db_user
