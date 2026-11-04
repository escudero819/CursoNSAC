# Clase 1 - FastAPI: Endpoints básicos

## 1. Explicación del ejemplo

En esta clase aprendes a crear una **API REST local** con **FastAPI**, la librería más rápida y moderna para construir APIs en Python.

El archivo `app.py` define cuatro endpoints:

1. `GET /` → Mensaje de bienvenida.
2. `GET /asteroides` → Lista completa de asteroides.
3. `GET /asteroide/{id}` → Un asteroide específico por su ID (parámetro de ruta).
4. `GET /buscar?nombre=...&peligroso=...` → Búsqueda con filtros opcionales (parámetros de consulta).

---

## 2. Explicación de la clase / conceptos clave

### ¿Qué es FastAPI?

FastAPI es un framework para crear APIs REST rápidamente. Ventajas:

- Muy rápido (rendimiento cercano a Node.js y Go).
- Validación automática de datos con Pydantic.
- Documentación automática en `/docs` (Swagger UI) y `/redoc`.
- Fácil de aprender y usar.

### Cómo ejecutar la API

```bash
uvicorn app:app --reload
```

- `app` es el nombre del archivo (`app.py`).
- `app` (después de los dos puntos) es el objeto `FastAPI` dentro del archivo.
- `--reload` reinicia el servidor automáticamente cuando guardas cambios.

Luego abre:
- `http://127.0.0.1:8000/` → Endpoint raíz
- `http://127.0.0.1:8000/docs` → Documentación interactiva (Swagger)
- `http://127.0.0.1:8000/asteroides` → Lista de asteroides

### Parámetros de ruta vs parámetros de consulta

| Tipo | Ejemplo | Para qué sirve |
|------|---------|----------------|
| Path parameter | `/asteroide/{asteroide_id}` | Identificar un recurso específico |
| Query parameter | `/buscar?nombre=Marte` | Filtrar o buscar resultados opcionales |

### Tipado en FastAPI

FastAPI usa anotaciones de tipo de Python (`int`, `str`, `bool`, `Optional`) para validar automáticamente lo que llega en la petición. Si el usuario envía un texto donde se espera un número, FastAPI devuelve un error 422 automáticamente.

---

## 3. Diccionario de sintaxis global - FastAPI (clase 1)

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Endpoint GET simple
@app.get("/")
def raiz():
    return {"mensaje": "Hola"}

# Con parametro de ruta
@app.get("/item/{item_id}")
def obtener_item(item_id: int):
    return {"id": item_id}

# Con parametro de consulta opcional
@app.get("/buscar")
def buscar(q: Optional[str] = None):
    return {"q": q}
```

---

## 4. Flujo de trabajo lógico

1. **Crear la app:** `app = FastAPI()`.
2. **Definir endpoints:** `@app.get("/ruta")` sobre una función.
3. **Definir parámetros:** Argumentos de la función con tipos (`int`, `str`, etc.).
4. **Retornar datos:** FastAPI convierte automáticamente el `return` a JSON.
5. **Ejecutar:** `uvicorn app:app --reload`.
6. **Probar:** Navegador, `/docs`, o `curl`.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: fastapi` | FastAPI no instalado | `pip install fastapi uvicorn` |
| Puerto 8000 en uso | Otro proceso usa el puerto | Cambiar puerto: `uvicorn app:app --port 8001` |
| Error 404 | Endpoint no existe | Revisar la URL y el decorador `@app.get(...)` |
| Error 422 | Tipo de dato incorrecto | Enviar el tipo correcto (ej. número para `int`) |

---

## 6. Adaptación a la competencia NSAC

En la hackathon, FastAPI te permite:

- Crear una API propia que tu equipo use para consultar los datos de la NASA guardados en SQLite.
- Exponer endpoints como `/asteroides/peligrosos` o `/eventos-naturales`.
- Que el frontend o otros integrantes consuman tus datos mediante HTTP.

Siguiente paso sugerido: `clase2_modelos_pydantic` para aprender a validar datos de entrada y salida con Pydantic.