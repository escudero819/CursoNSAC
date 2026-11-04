# Clase 4 - FastAPI: Integracion con API de la NASA
# Objetivo:
# - Crear endpoints que consuman la API de la NASA (requests).
# - Guardar los resultados en SQLite local (SQLAlchemy).
# - Evitar llamar a la NASA repetidamente (cache local en BD).
# - Endpoint para sincronizar datos manualmente.
# - Endpoint para consultar datos guardados localmente.
#
# Requisitos:
#   pip install fastapi uvicorn requests sqlalchemy pandas
#
# Como ejecutar:
#   uvicorn app:app --reload
#
# Documentacion:
#   http://127.0.0.1:8000/docs

import requests
import pandas as pd
from datetime import date, timedelta, datetime
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional


# --- Configuracion ---
NASA_BASE_URL = "https://api.nasa.gov"
API_KEY = "DEMO_KEY"
RUTA_BD = "sqlite:///./recursos/datos_nasa_api.db"

engine = create_engine(RUTA_BD, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Modelo SQLAlchemy ---
class EventoNasaDB(Base):
    __tablename__ = "eventos_nasa"

    id = Column(Integer, primary_key=True, index=True)
    fuente = Column(String(50), nullable=False)  # ej. "EONET", "NEO", "APOD"
    titulo = Column(String(200), nullable=False)
    descripcion = Column(String(1000))
    fecha_evento = Column(Date, nullable=False)
    url_origen = Column(String(500))
    fecha_guardado = Column(Date, default=date.today)


# --- Modelos Pydantic ---
class EventoNasaBase(BaseModel):
    fuente: str
    titulo: str = Field(..., min_length=3)
    descripcion: Optional[str] = None
    fecha_evento: date
    url_origen: Optional[str] = None


class EventoNasaRespuesta(EventoNasaBase):
    id: int
    fecha_guardado: date

    class Config:
        from_attributes = True


class SincronizacionRespuesta(BaseModel):
    mensaje: str
    eventos_sincronizados: int


# --- Dependencia BD ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API NSAC - Integracion NASA", version="1.0.0")


# --- Funciones auxiliares ---

def obtener_eventos_eonet(limite: int = 10):
    # Consulta la API EONET de la NASA (eventos naturales: volcanes, incendios, tormentas).
    url = NASA_BASE_URL + "/EONET/v2.1/events"
    params = {"api_key": API_KEY, "limit": limite, "status": "open"}

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        datos = response.json()
        return datos.get("events", [])
    except requests.exceptions.RequestException as e:
        print("Error consultando EONET: " + str(e))
        return []


def guardar_eventos_en_bd(eventos, db: Session):
    # Guarda eventos en SQLite evitando duplicados (por titulo + fecha).
    insertados = 0
    for ev in eventos:
        titulo = ev.get("title", "Sin titulo")
        fecha_str = ev.get("date", "")
        try:
            fecha_evento = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            fecha_evento = date.today()

        existe = db.query(EventoNasaDB).filter(
            EventoNasaDB.titulo == titulo,
            EventoNasaDB.fecha_evento == fecha_evento
        ).first()

        if existe:
            continue

        nuevo = EventoNasaDB(
            fuente="EONET",
            titulo=titulo,
            descripcion=ev.get("description", ""),
            fecha_evento=fecha_evento,
            url_origen=ev.get("link", "")
        )
        db.add(nuevo)
        insertados += 1

    db.commit()
    return insertados


# --- Endpoints ---

@app.get("/")
def raiz():
    return {"mensaje": "API NASA integrada - Endpoints de eventos espaciales"}


@app.get("/eventos", response_model=List[EventoNasaRespuesta])
def listar_eventos(
    db: Session = Depends(get_db),
    fuente: Optional[str] = None,
    limite: int = 50
):
    # Lista eventos guardados localmente en SQLite.
    # Filtro opcional por fuente (ej. "EONET").
    query = db.query(EventoNasaDB)
    if fuente:
        query = query.filter(EventoNasaDB.fuente == fuente)
    return query.limit(limite).all()


@app.post("/sincronizar-nasa", response_model=SincronizacionRespuesta)
def sincronizar_nasa(
    background_tasks: BackgroundTasks,
    limite: int = 10,
    db: Session = Depends(get_db)
):
    # Sincroniza eventos desde la API de la NASA (EONET) y los guarda en SQLite.
    # Se ejecuta en segundo plano (BackgroundTasks) para no bloquear la respuesta.
    eventos = obtener_eventos_eonet(limite=limite)
    if not eventos:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudieron obtener datos de la NASA en este momento"
        )

    insertados = guardar_eventos_en_bd(eventos, db)

    return SincronizacionRespuesta(
        mensaje="Sincronizacion completada",
        eventos_sincronizados=insertados
    )


@app.get("/eventos/{evento_id}", response_model=EventoNasaRespuesta)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    # Obtiene un evento por su ID local.
    evento = db.query(EventoNasaDB).filter(EventoNasaDB.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@app.delete("/eventos/{evento_id}")
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    # Elimina un evento guardado localmente.
    evento = db.query(EventoNasaDB).filter(EventoNasaDB.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado para eliminar")
    db.delete(evento)
    db.commit()
    return {"mensaje": "Evento " + str(evento_id) + " eliminado"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)