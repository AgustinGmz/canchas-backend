from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

app = FastAPI(title="Sistema de Reservas de Canchas API")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Reservas de Canchas Backend"}

# CRUD Usuarios
@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    new_user = models.Usuario(**usuario.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/usuarios/", response_model=List[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

# CRUD Canchas
@app.post("/canchas/", response_model=schemas.Cancha)
def create_cancha(cancha: schemas.CanchaCreate, db: Session = Depends(get_db)):
    new_cancha = models.Cancha(**cancha.model_dump())
    db.add(new_cancha)
    db.commit()
    db.refresh(new_cancha)
    return new_cancha

@app.get("/canchas/", response_model=List[schemas.Cancha])
def read_canchas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Cancha).offset(skip).limit(limit).all()

@app.get("/canchas/{cancha_id}", response_model=schemas.Cancha)
def read_cancha(cancha_id: int, db: Session = Depends(get_db)):
    db_cancha = db.query(models.Cancha).filter(models.Cancha.id == cancha_id).first()
    if db_cancha is None:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    return db_cancha

@app.put("/canchas/{cancha_id}", response_model=schemas.Cancha)
def update_cancha(cancha_id: int, cancha: schemas.CanchaCreate, db: Session = Depends(get_db)):
    db_cancha = db.query(models.Cancha).filter(models.Cancha.id == cancha_id).first()
    if db_cancha is None:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    for key, value in cancha.model_dump().items():
        setattr(db_cancha, key, value)
    db.commit()
    db.refresh(db_cancha)
    return db_cancha

@app.delete("/canchas/{cancha_id}")
def delete_cancha(cancha_id: int, db: Session = Depends(get_db)):
    db_cancha = db.query(models.Cancha).filter(models.Cancha.id == cancha_id).first()
    if db_cancha is None:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    db.delete(db_cancha)
    db.commit()
    return {"ok": True}
