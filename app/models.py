from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Cancha(Base):
    __tablename__ = "canchas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String)  # ej. Futbol, Basquetbol, Tenis
    precio_hora = Column(Float)
