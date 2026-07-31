from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class CanchaBase(BaseModel):
    nombre: str
    tipo: str
    precio_hora: float

class CanchaCreate(CanchaBase):
    pass

class Cancha(CanchaBase):
    id: int

    class Config:
        from_attributes = True
