# Clase 3 - FastAPI: CRUD con base de datos SQLite
# Objetivo:
# - Conectar FastAPI con SQLite mediante SQLAlchemy.
# - Implementar CRUD completo (Create, Read, Update, Delete) persistente.
# - Usar sesiones de base de datos por peticion (dependency injection).
# - Exponer endpoints que leen y escriben en la BD local.
#
# Requisitos:
#   pip install fastapi uvicorn sqlalchemy
#
# Como ejecutar:
#   uvicorn app:app --reload
#
# Documentacion:
#   http://127.0.0.1:8000/docs

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


# --- Configuracion de base de datos ---
RUTA_BD = "sqlite:///./recursos/datos_fastapi.db"
engine = create_engine(RUTA_BD, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Modelo SQLAlchemy (tabla en BD) ---
class AsteroideDB(Base):
    __tablename__ = "asteroides"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    diametro_km = Column(Float, nullable=False)
    peligroso = Column(Boolean, default=False)
    fecha_acercamiento = Column(Date, nullable=False)


# --- Modelos Pydantic (validacion de API) ---
class AsteroideBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    diametro_km: float = Field(..., gt=0)
    peligroso: bool = Field(default=False)
    fecha_acercamiento: date


class AsteroideCrear(AsteroideBase):
    pass


class AsteroideRespuesta(AsteroideBase):
    id: int

    class Config:
        from_attributes = True  # Permite leer desde objetos SQLAlchemy


# --- Dependencia para obtener sesion de BD ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)


# --- App FastAPI ---
app = FastAPI(title="API NSAC - CRUD con SQLite", version="1.0.0")


@app.get("/")
def raiz():
    return {"mensaje": "API CRUD con SQLite y FastAPI"}


@app.post("/asteroides", response_model=AsteroideRespuesta, status_code=status.HTTP_201_CREATED)
def crear_asteroide(asteroide: AsteroideCrear, db: Session = Depends(get_db)):
    # Crea un nuevo asteroide en la base de datos.
    db_asteroide = AsteroideDB(
        nombre=asteroide.nombre,
        diametro_km=asteroide.diametro_km,
        peligroso=asteroide.peligroso,
        fecha_acercamiento=asteroide.fecha_acercamiento
    )
    db.add(db_asteroide)
    db.commit()
    db.refresh(db_asteroide)
    return db_asteroide


@app.get("/asteroides", response_model=List[AsteroideRespuesta])
def listar_asteroides(db: Session = Depends(get_db), peligroso: Optional[bool] = None):
    # Lista todos los asteroides. Opcionalmente filtrar por peligroso.
    query = db.query(AsteroideDB)
    if peligroso is not None:
        query = query.filter(AsteroideDB.peligroso == peligroso)
    return query.all()


@app.get("/asteroides/{asteroide_id}", response_model=AsteroideRespuesta)
def obtener_asteroide(asteroide_id: int, db: Session = Depends(get_db)):
    # Obtiene un asteroide por su ID.
    asteroide = db.query(AsteroideDB).filter(AsteroideDB.id == asteroide_id).first()
    if not asteroide:
        raise HTTPException(status_code=404, detail="Asteroide no encontrado")
    return asteroide


@app.put("/asteroides/{asteroide_id}", response_model=AsteroideRespuesta)
def actualizar_asteroide(asteroide_id: int, datos: AsteroideCrear, db: Session = Depends(get_db)):
    # Actualiza un asteroide existente.
    asteroide = db.query(AsteroideDB).filter(AsteroideDB.id == asteroide_id).first()
    if not asteroide:
        raise HTTPException(status_code=404, detail="Asteroide no encontrado para actualizar")

    asteroide.nombre = datos.nombre
    asteroide.diametro_km = datos.diametro_km
    asteroide.peligroso = datos.peligroso
    asteroide.fecha_acercamiento = datos.fecha_acercamiento

    db.commit()
    db.refresh(asteroide)
    return asteroide


@app.delete("/asteroides/{asteroide_id}")
def eliminar_asteroide(asteroide_id: int, db: Session = Depends(get_db)):
    # Elimina un asteroide por su ID.
    asteroide = db.query(AsteroideDB).filter(AsteroideDB.id == asteroide_id).first()
    if not asteroide:
        raise HTTPException(status_code=404, detail="Asteroide no encontrado para eliminar")

    db.delete(asteroide)
    db.commit()
    return {"mensaje": "Asteroide " + str(asteroide_id) + " eliminado correctamente"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)