# Clase 3 - FastAPI: CRUD con SQLite

## 1. Explicación del ejemplo

En esta clase conectas **FastAPI** con **SQLite** mediante **SQLAlchemy** para crear una API REST persistente. Los datos ya no se pierden cuando reinicias el servidor, porque se guardan en un archivo `.db`.

El archivo `app.py` implementa un CRUD completo:

- **POST /asteroides** → Crear (Create)
- **GET /asteroides** → Leer todos (Read), con filtro opcional por `peligroso`
- **GET /asteroides/{id}** → Leer uno (Read)
- **PUT /asteroides/{id}** → Actualizar (Update)
- **DELETE /asteroides/{id}** → Eliminar (Delete)

Además usa **dependency injection** (`Depends(get_db)`) para manejar la sesión de base de datos por cada petición.

---

## 2. Explicación de la clase / conceptos clave

### SQLAlchemy + FastAPI

Separamos dos capas:

| Capa | Clase | Propósito |
|------|-------|-----------|
| Base de datos | `AsteroideDB` (hereda de `Base`) | Define la tabla en SQLite |
| API / Validación | `AsteroideCrear`, `AsteroideRespuesta` (Pydantic) | Valida entrada y salida de la API |

### Dependency Injection con `Depends(get_db)`

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Cada petición recibe su propia sesión de base de datos, y se cierra automáticamente al terminar. Esto evita fugas de conexiones y problemas de concurrencia en SQLite.

### `from_attributes = True`

En Pydantic v2, permite que el modelo lea datos directamente de un objeto SQLAlchemy:

```python
class AsteroideRespuesta(AsteroideBase):
    id: int
    class Config:
        from_attributes = True
```

### Operaciones CRUD con SQLAlchemy

| Operación | Código SQLAlchemy |
|-----------|-------------------|
| Insertar | `db.add(obj)`, `db.commit()`, `db.refresh(obj)` |
| Consultar todos | `db.query(Modelo).all()` |
| Consultar uno | `db.query(Modelo).filter(Modelo.id == id).first()` |
| Actualizar | Modificar atributos, `db.commit()`, `db.refresh(obj)` |
| Eliminar | `db.delete(obj)`, `db.commit()` |

---

## 3. Diccionario de sintaxis global - FastAPI + SQLAlchemy

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

engine = create_engine("sqlite:///datos.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ModeloDB(Base):
    __tablename__ = "tabla"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))

class Entrada(BaseModel):
    nombre: str

class Salida(Entrada):
    id: int
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/items", response_model=Salida)
def crear(item: Entrada, db: Session = Depends(get_db)):
    obj = ModeloDB(**item.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
```

---

## 4. Flujo de trabajo lógico

1. **Configurar BD:** `create_engine`, `sessionmaker`, `declarative_base`.
2. **Definir modelo DB:** Clase con `__tablename__` y columnas.
3. **Definir modelos Pydantic:** Entrada y respuesta.
4. **Crear tablas:** `Base.metadata.create_all(bind=engine)`.
5. **Definir dependencia `get_db`:** Para sesiones por petición.
6. **Crear endpoints CRUD:** Usar `Depends(get_db)` en cada endpoint.
7. **Probar:** Ir a `/docs` y probar cada endpoint.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `OperationalError: unable to open database file` | Ruta sin permisos de escritura | Verificar que la carpeta `recursos/` existe |
| `sqlalchemy.exc.IntegrityError` | Violación de restricción (NOT NULL, UNIQUE) | Revisar que se envían todos los campos obligatorios |
| Sesión no cierra | Se olvida `db.close()` | Usar `Depends(get_db)` con `try/finally` |
| `check_same_thread` error | SQLite con FastAPI en hilos múltiples | Agregar `connect_args={"check_same_thread": False}` al engine |

---

## 6. Adaptación a la competencia NSAC

Este es el puente final entre tus datos y el equipo:

- Guarda los datos de la NASA en SQLite (desde la clase anterior de integración).
- Expón endpoints para que el equipo consulte asteroides peligrosos, eventos naturales, etc.
- Otros integrantes pueden consumir tu API desde el frontend o desde sus propios scripts.

Siguiente paso sugerido: `clase4_integracion_nasa_endpoints` para crear endpoints que consuman la API de la NASA y guarden los resultados en tu BD local.