# Diccionario de sintaxis rápida - `FastAPI` + `Pydantic`

## Instalación
```bash
pip install fastapi uvicorn
```

## Ejecutar servidor
```bash
uvicorn app:app --reload
```
- `app:app` = archivo `app.py`, objeto `app`
- `--reload` = reinicia automáticamente al guardar

## Crear la aplicación

```python
from fastapi import FastAPI
app = FastAPI(title="Mi API", version="1.0.0")
```

## Endpoints básicos

| Método | Decorador | Uso |
|--------|-----------|-----|
| GET | `@app.get("/ruta")` | Obtener datos |
| POST | `@app.post("/ruta")` | Crear datos |
| PUT | `@app.put("/ruta/{id}")` | Actualizar datos |
| DELETE | `@app.delete("/ruta/{id}")` | Eliminar datos |

```python
@app.get("/")
def raiz():
    return {"mensaje": "Hola"}

@app.get("/item/{item_id}")
def obtener_item(item_id: int):
    return {"id": item_id}

@app.get("/buscar")
def buscar(q: Optional[str] = None):
    return {"q": q}
```

## Parámetros

| Tipo | Sintaxis | Ejemplo |
|------|----------|---------|
| Path parameter | `def f(item_id: int):` | `/item/{item_id}` |
| Query parameter | `def f(q: Optional[str] = None):` | `/buscar?q=texto` |
| Body (Pydantic) | `def f(datos: Modelo):` | POST con JSON |

## Pydantic (validación de datos)

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class Entrada(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    edad: int = Field(..., gt=0, le=120)
    email: Optional[str] = None

class Salida(Entrada):
    id: int
    class Config:
        from_attributes = True  # Leer desde objetos SQLAlchemy
```

## Usar modelos en endpoints

```python
@app.post("/items", response_model=Salida, status_code=status.HTTP_201_CREATED)
def crear_item(datos: Entrada):
    return datos

@app.get("/items", response_model=List[Salida])
def listar_items():
    return []
```

## Errores HTTP personalizados

```python
from fastapi import HTTPException, status

raise HTTPException(status_code=404, detail="No encontrado")
raise HTTPException(status_code=422, detail="Dato inválido")
```

## FastAPI + SQLAlchemy (CRUD persistente)

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items", response_model=Salida)
def crear(item: Entrada, db: Session = Depends(get_db)):
    obj = ModeloDB(**item.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
```

## Documentación automática

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

> **Tip:** Pydantic valida automáticamente los datos de entrada. Si están mal, FastAPI devuelve error 422 sin que tengas que escribir validaciones manuales.