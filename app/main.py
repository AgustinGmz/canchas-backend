from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

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
def read_canchas(skip: int = 0, limit: int = 100, tipo: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Cancha)
    if tipo:
        query = query.filter(models.Cancha.tipo.ilike(f"%{tipo}%"))
    return query.offset(skip).limit(limit).all()

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

# CRUD Reservas
@app.post("/reservas/", response_model=schemas.Reserva)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    # Regla de negocio: Verificar si la cancha está disponible
    cancha = db.query(models.Cancha).filter(models.Cancha.id == reserva.cancha_id).first()
    if not cancha:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    if not cancha.disponible:
        raise HTTPException(status_code=400, detail="La cancha no está disponible para reserva")
    
    usuario = db.query(models.Usuario).filter(models.Usuario.id == reserva.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    new_reserva = models.Reserva(**reserva.model_dump())
    db.add(new_reserva)
    db.commit()
    db.refresh(new_reserva)
    return new_reserva

@app.get("/reservas/", response_model=List[schemas.Reserva])
def read_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Reserva).offset(skip).limit(limit).all()

@app.get("/reservas/{reserva_id}", response_model=schemas.Reserva)
def read_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@app.put("/reservas/{reserva_id}", response_model=schemas.Reserva)
def update_reserva(reserva_id: int, reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Check new cancha
    if reserva.cancha_id != db_reserva.cancha_id:
        cancha = db.query(models.Cancha).filter(models.Cancha.id == reserva.cancha_id).first()
        if not cancha:
            raise HTTPException(status_code=404, detail="Nueva cancha no encontrada")
        if not cancha.disponible:
            raise HTTPException(status_code=400, detail="La nueva cancha no está disponible")
            
    for key, value in reserva.model_dump().items():
        setattr(db_reserva, key, value)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

@app.delete("/reservas/{reserva_id}")
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    db.delete(db_reserva)
    db.commit()
    return {"ok": True}
