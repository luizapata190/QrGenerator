from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    cedula: str
    nombre: str
    email: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
