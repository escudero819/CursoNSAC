# Clase 1 - Sistema integrado: NASA + pandas + SQLite + FastAPI

## 1. Explicación del ejemplo

Esta clase une **todas las librerías del curso** en un solo sistema real, listo para usar en la hackathon NSAC. El archivo `app.py` implementa un flujo completo:

1. **Extraer (requests):** Consulta dos endpoints de la NASA (NeoWs para asteroides y EONET para eventos naturales).
2. **Transformar (pandas):** Convierte los JSON recibidos en DataFrames planos, limpia datos y calcula estadísticas.
3. **Cargar (SQLAlchemy + SQLite):** Guarda los eventos en una base de datos local, evitando duplicados.
4. **Exponer (FastAPI):** Crea endpoints REST para consultar, filtrar, obtener, eliminar y exportar los datos almacenados.

Además, incluye un endpoint de estadísticas que lee desde SQLite con SQLAlchemy, convierte a DataFrame con pandas y calcula métricas, mostrando cómo las librerías trabajan juntas en un mismo programa.

---

## 2. Explicación de la clase / conceptos clave

### Arquitectura del sistema integrado

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   NASA API      │────▶│   requests      │────▶│   JSON crudo    │
│  (NeoWs, EONET) │     │   (HTTP)        │     │   (Extraer)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Estadísticas   │◄────│   pandas        │◄────│   DataFrame     │
│  (total, por    │     │   (Transformar) │     │   (Limpiar)     │
│   fuente, etc.) │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Endpoints      │◄────│  FastAPI        │◄────│   SQLite        │
│  REST (/eventos │     │   (Exponer)     │     │   (Cargar)      │
│   /sincronizar  │     │                 │     │   SQLAlchemy    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### ¿Por qué integrar todo en un sistema?

En una hackathon, no usas una librería de forma aislada. El flujo real es:

1. Consigues datos de la NASA con `requests`.
2. Los limpias y estructuras con `pandas`.
3. Los guardas en `SQLite` para no llamar a la API otra vez.
4. Los expones con `FastAPI` para que el resto del equipo los use.

### Evitar llamadas repetidas (caché local)

El endpoint `/sincronizar-nasa` consulta la NASA y guarda en SQLite. Los endpoints posteriores (`/eventos`, `/estadisticas`, `/exportar-csv`) leen desde la base de datos local, no de la NASA. Esto:

- Ahorra peticiones a la API (evita el rate limit).
- Hace que el sistema sea más rápido (SQLite local es más rápido que HTTP).
- Te permite seguir trabajando aunque la NASA esté caída.

### Evitar duplicados

Antes de insertar cada evento, el sistema verifica si ya existe uno con la misma fuente, nombre y fecha. Si existe, lo omite y lo cuenta como duplicado.

---

## 3. Diccionario de sintaxis global - Sistema integrado

```python
import requests
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

# 1. Conexión a SQLite
engine = create_engine("sqlite:///sistema.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# 2. Modelo de tabla
class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200))
    fuente = Column(String(50))

Base.metadata.create_all(engine)

# 3. Dependency de sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. Modelo Pydantic
class EventoRespuesta(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

# 5. App FastAPI
app = FastAPI()

@app.get("/eventos", response_model=List[EventoRespuesta])
def listar(db: Session = Depends(get_db)):
    return db.query(Evento).all()

# 6. Extraer de NASA
response = requests.get("https://api.nasa.gov/...", params=params, timeout=20)
datos = response.json()

# 7. Transformar con pandas
df = pd.DataFrame(datos_limpios)

# 8. Exportar
df.to_csv("export.csv", index=False)
```

---

## 4. Flujo de trabajo lógico para la competencia NSAC

1. **Definir el modelo de datos:** ¿Qué información necesitas guardar? (nombre, fecha, fuente, peligroso, etc.)
2. **Crear las tablas:** SQLAlchemy define la estructura en SQLite.
3. **Sincronizar datos:** `requests` consulta la NASA, `pandas` transforma, SQLAlchemy guarda en SQLite.
4. **Exponer endpoints:** FastAPI permite que el equipo consulte los datos sin conocer la API de la NASA.
5. **Exportar si es necesario:** `pandas` puede exportar a CSV/Excel para presentaciones.
6. **Calcular estadísticas:** `pandas` sobre los datos de SQLite da métricas rápidas para el jurado.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| API de la NASA no responde | Sin internet o servidor caído | `try/except` + `HTTPException 503`; usar datos locales guardados |
| Límite de peticiones (429) | Demasiadas llamadas a la NASA | Sincroniza menos seguido; usa caché en SQLite |
| Base de datos bloqueada | Escritura concurrente en SQLite | Cerrar sesiones correctamente con `get_db` |
| Datos duplicados | Sincronizar dos veces mismo rango | Verificar existencia antes de `session.add()` |
| Puerto 8000 ocupado | Otro proceso usa el puerto | Cambiar puerto: `uvicorn app:app --port 8001` |

---

## 6. Adaptación a la competencia NSAC

Este sistema es la base de tu entrega en la hackathon:

- **Tu equipo** consulta `/eventos` para ver datos sin depender de internet.
- **Tú** ejecutas `/sincronizar-nasa` antes de la presentación para tener datos frescos.
- **Puedes exportar** a CSV con `/exportar-csv` para incluir en el informe.
- **Las estadísticas** (`/estadisticas`) dan números clave para el jurado (total de eventos, cuántos son peligrosos, por fuente).

Este es el caso real completo: datos de la NASA → procesamiento → base de datos local → API para el equipo.