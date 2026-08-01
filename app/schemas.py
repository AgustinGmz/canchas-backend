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
    disponible: bool = True

class CanchaCreate(CanchaBase):
    pass

class Cancha(CanchaBase):
    id: int

    class Config:
        from_attributes = True

class ReservaBase(BaseModel):
    usuario_id: int
    cancha_id: int
    fecha: str

class ReservaCreate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id: int

    class Config:
        from_attributes = True
