# Clase 1 - Sistema integrado: NASA + pandas + SQLite + FastAPI
# Objetivo:
# - Unir todas las librerías del curso en un sistema real y coherente.
# - Flujo ETL: Extraer (requests) -> Transformar (pandas) -> Cargar (SQLAlchemy/SQLite).
# - Exponer los datos almacenados mediante endpoints FastAPI.
# - Evitar llamadas repetidas a la NASA usando caché local en SQLite.
#
# Requisitos:
#   pip install requests pandas sqlalchemy fastapi uvicorn
#
# Como ejecutar:
#   uvicorn app:app --reload
#
# Documentación:
#   http://127.0.0.1:8000/docs

import requests
import pandas as pd
from datetime import date, timedelta, datetime
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional


# ============================================================================
# CONFIGURACIÓN GENERAL DEL SISTEMA
# ============================================================================
NASA_BASE_URL = "https://api.nasa.gov"
API_KEY = "DEMO_KEY"  # Reemplaza por tu propia key de api.nasa.gov
RUTA_BD = "sqlite:///./recursos/sistema_integrado.db"

engine = create_engine(RUTA_BD, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="Sistema Integrado NSAC - Datos Espaciales",
    version="1.0.0",
    description="Sistema que integra requests, pandas, SQLAlchemy y FastAPI para la hackathon NASA Space Apps"
)


# ============================================================================
# MODELO SQLALCHEMY (Tabla en SQLite)
# ============================================================================
class EventoEspacialDB(Base):
    __tablename__ = "eventos_espaciales"

    id = Column(Integer, primary_key=True, index=True)
    fuente = Column(String(50), nullable=False)          # "NEO", "EONET", "APOD"
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(1000))
    fecha_evento = Column(Date, nullable=False)
    diametro_km = Column(Float)
    peligroso = Column(Boolean, default=False)
    distancia_km = Column(Float)
    velocidad_km_h = Column(Float)
    url_origen = Column(String(500))
    fecha_guardado = Column(Date, default=date.today)


# ============================================================================
# MODELOS PYDANTIC (Validación de API)
# ============================================================================
class EventoBase(BaseModel):
    fuente: str
    nombre: str = Field(..., min_length=3, max_length=200)
    descripcion: Optional[str] = None
    fecha_evento: date
    diametro_km: Optional[float] = None
    peligroso: bool = Field(default=False)
    distancia_km: Optional[float] = None
    velocidad_km_h: Optional[float] = None
    url_origen: Optional[str] = None


class EventoCrear(EventoBase):
    pass


class EventoRespuesta(EventoBase):
    id: int
    fecha_guardado: date

    class Config:
        from_attributes = True


class SincronizacionRespuesta(BaseModel):
    mensaje: str
    eventos_sincronizados: int
    eventos_omitidos_duplicados: int


class EstadisticasRespuesta(BaseModel):
    total_eventos: int
    eventos_peligrosos: int
    eventos_por_fuente: dict


# ============================================================================
# DEPENDENCY INJECTION - Sesión de base de datos por petición
# ============================================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)


# ============================================================================
# FUNCIONES AUXILIARES DEL SISTEMA
# ============================================================================

def consultar_nasa_neos(fecha_inicio: str, fecha_fin: str):
    """
    Extrae datos de la API NeoWs de la NASA (asteroides cercanos).
    Retorna la lista de asteroides o una lista vacía si hay error.
    """
    url = f"{NASA_BASE_URL}/neo/rest/v1/feed"
    params = {
        "api_key": API_KEY,
        "start_date": fecha_inicio,
        "end_date": fecha_fin
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        datos = response.json()
        cercanias = datos.get("near_earth_objects", {})
        lista_asteroides = []
        for fecha_str, asteroides in cercanias.items():
            for ast in asteroides:
                diametro = ast.get("estimated_diameter", {}).get("kilometers", {})
                acercamientos = ast.get("close_approach_data", [])
                vel = acercamientos[0].get("relative_velocity", {}).get("kilometers_per_hour") if acercamientos else None
                dist = acercamientos[0].get("miss_distance", {}).get("kilometers") if acercamientos else None
                lista_asteroides.append({
                    "fuente": "NEO",
                    "nombre": ast.get("name", "Desconocido"),
                    "descripcion": f"Asteroide cercano a la Tierra. Magnitud absoluta: {ast.get('absolute_magnitude_h', 'N/A')}",
                    "fecha_evento": fecha_str,
                    "diametro_km": diametro.get("estimated_diameter_max"),
                    "peligroso": ast.get("is_potentially_hazardous_asteroid", False),
                    "distancia_km": dist,
                    "velocidad_km_h": vel,
                    "url_origen": "https://api.nasa.gov"
                })
        return lista_asteroides
    except requests.exceptions.RequestException as e:
        print(f"Error consultando NeoWs: {e}")
        return []


def consultar_nasa_eonet(limite: int = 10):
    """
    Extrae datos de la API EONET de la NASA (eventos naturales).
    """
    url = f"{NASA_BASE_URL}/EONET/v2.1/events"
    params = {"api_key": API_KEY, "limit": limite, "status": "open"}

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        datos = response.json()
        lista_eventos = []
        for ev in datos.get("events", []):
            fecha_str = ev.get("date", "")
            try:
                fecha_evento = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except Exception:
                fecha_evento = date.today()
            lista_eventos.append({
                "fuente": "EONET",
                "nombre": ev.get("title", "Sin título"),
                "descripcion": ev.get("description", ""),
                "fecha_evento": fecha_evento.isoformat(),
                "diametro_km": None,
                "peligroso": False,
                "distancia_km": None,
                "velocidad_km_h": None,
                "url_origen": ev.get("link", "")
            })
        return lista_eventos
    except requests.exceptions.RequestException as e:
        print(f"Error consultando EONET: {e}")
        return []


def guardar_eventos_en_bd(eventos: list, db: Session):
    """
    Guarda eventos en SQLite evitando duplicados (por fuente + nombre + fecha).
    Retorna (insertados, omitidos).
    """
    insertados = 0
    omitidos = 0

    for ev in eventos:
        fecha_str = ev["fecha_evento"]
        try:
            fecha_evento = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            fecha_evento = date.today()

        existe = db.query(EventoEspacialDB).filter(
            EventoEspacialDB.fuente == ev["fuente"],
            EventoEspacialDB.nombre == ev["nombre"],
            EventoEspacialDB.fecha_evento == fecha_evento
        ).first()

        if existe:
            omitidos += 1
            continue

        nuevo = EventoEspacialDB(
            fuente=ev["fuente"],
            nombre=ev["nombre"],
            descripcion=ev.get("descripcion", ""),
            fecha_evento=fecha_evento,
            diametro_km=ev.get("diametro_km"),
            peligroso=bool(ev.get("peligroso", False)),
            distancia_km=ev.get("distancia_km"),
            velocidad_km_h=ev.get("velocidad_km_h"),
            url_origen=ev.get("url_origen", "")
        )
        db.add(nuevo)
        insertados += 1

    db.commit()
    return insertados, omitidos


def transformar_a_dataframe(db: Session) -> pd.DataFrame:
    """
    Lee la tabla de eventos y la convierte en un DataFrame de pandas.
    """
    registros = db.query(EventoEspacialDB).all()
    if not registros:
        return pd.DataFrame()

    datos = []
    for r in registros:
        datos.append({
            "id": r.id,
            "fuente": r.fuente,
            "nombre": r.nombre,
            "descripcion": r.descripcion,
            "fecha_evento": r.fecha_evento,
            "diametro_km": r.diametro_km,
            "peligroso": r.peligroso,
            "distancia_km": r.distancia_km,
            "velocidad_km_h": r.velocidad_km_h,
            "fecha_guardado": r.fecha_guardado
        })

    return pd.DataFrame(datos)


# ============================================================================
# ENDPOINTS FASTAPI
# ============================================================================

@app.get("/")
def raiz():
    return {
        "mensaje": "Sistema Integrado NSAC - Datos Espaciales",
        "version": "1.0.0",
        "endpoints": {
            "documentacion": "/docs",
            "sincronizar_nasa": "/sincronizar-nasa",
            "listar_eventos": "/eventos",
            "obtener_evento": "/eventos/{id}",
            "estadisticas": "/estadisticas",
            "eliminar_evento": "/eventos/{id}"
        }
    }


@app.post("/sincronizar-nasa", response_model=SincronizacionRespuesta)
def sincronizar_nasa(
    background_tasks: BackgroundTasks,
    dias: int = 7,
    limite_eonet: int = 10,
    db: Session = Depends(get_db)
):
    """
    Sincroniza eventos desde la API de la NASA (NeoWs y EONET)
    y los guarda en SQLite local como caché.
    """
    hoy = date.today()
    hace_dias = hoy - timedelta(days=dias)

    # Extraer de NeoWs (asteroides)
    eventos_neo = consultar_nasa_neos(str(hace_dias), str(hoy))

    # Extraer de EONET (eventos naturales)
    eventos_eonet = consultar_nasa_eonet(limite=limite_eonet)

    todos_los_eventos = eventos_neo + eventos_eonet

    if not todos_los_eventos:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudieron obtener datos de la NASA en este momento"
        )

    insertados, omitidos = guardar_eventos_en_bd(todos_los_eventos, db)

    return SincronizacionRespuesta(
        mensaje="Sincronización completada",
        eventos_sincronizados=insertados,
        eventos_omitidos_duplicados=omitidos
    )


@app.get("/eventos", response_model=List[EventoRespuesta])
def listar_eventos(
    db: Session = Depends(get_db),
    fuente: Optional[str] = None,
    peligroso: Optional[bool] = None,
    limite: int = 50
):
    """
    Lista eventos guardados localmente en SQLite.
    Filtros opcionales por fuente y si es peligroso.
    """
    query = db.query(EventoEspacialDB)
    if fuente:
        query = query.filter(EventoEspacialDB.fuente == fuente)
    if peligroso is not None:
        query = query.filter(EventoEspacialDB.peligroso == peligroso)
    return query.limit(limite).all()


@app.get("/eventos/{evento_id}", response_model=EventoRespuesta)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    """Obtiene un evento por su ID local."""
    evento = db.query(EventoEspacialDB).filter(EventoEspacialDB.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@app.delete("/eventos/{evento_id}")
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    """Elimina un evento guardado localmente."""
    evento = db.query(EventoEspacialDB).filter(EventoEspacialDB.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado para eliminar")
    db.delete(evento)
    db.commit()
    return {"mensaje": f"Evento {evento_id} eliminado correctamente"}


@app.get("/estadisticas", response_model=EstadisticasRespuesta)
def estadisticas(db: Session = Depends(get_db)):
    """
    Devuelve estadísticas de los eventos guardados en SQLite,
    calculadas con pandas sobre los datos leídos de la base.
    """
    df = transformar_a_dataframe(db)

    if df.empty:
        return EstadisticasRespuesta(
            total_eventos=0,
            eventos_peligrosos=0,
            eventos_por_fuente={}
        )

    total = len(df)
    peligrosos = int(df["peligroso"].sum()) if "peligroso" in df.columns else 0

    # Conteo por fuente usando pandas
    por_fuente = {}
    if "fuente" in df.columns:
        conteo_fuente = df["fuente"].value_counts().to_dict()
        por_fuente = {str(k): int(v) for k, v in conteo_fuente.items()}

    return EstadisticasRespuesta(
        total_eventos=total,
        eventos_peligrosos=peligrosos,
        eventos_por_fuente=por_fuente
    )


@app.get("/exportar-csv")
def exportar_csv(db: Session = Depends(get_db)):
    """
    Exporta los eventos guardados en SQLite a un archivo CSV usando pandas.
    """
    df = transformar_a_dataframe(db)
    if df.empty:
        raise HTTPException(status_code=404, detail="No hay datos para exportar")

    nombre_archivo = "recursos/eventos_exportados.csv"
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")
    return {
        "mensaje": f"Datos exportados a {nombre_archivo}",
        "filas_exportadas": len(df)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)