from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    
    reservas = relationship("Reserva", back_populates="usuario")

class Cancha(Base):
    __tablename__ = "canchas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String)  # ej. Futbol, Basquetbol, Tenis
    precio_hora = Column(Float)
    disponible = Column(Boolean, default=True)
    
    reservas = relationship("Reserva", back_populates="cancha")

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cancha_id = Column(Integer, ForeignKey("canchas.id"))
    fecha = Column(String)
    
    usuario = relationship("Usuario", back_populates="reservas")
    cancha = relationship("Cancha", back_populates="reservas")
