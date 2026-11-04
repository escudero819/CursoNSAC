# Clase 2 - FastAPI: Modelos Pydantic

## 1. Explicación del ejemplo

En esta clase aprendes a usar **Pydantic** (integrado en FastAPI) para validar los datos que entran y salen de tu API. Esto es fundamental en una hackathon para evitar que datos incorrectos rompan tu programa.

El archivo `app.py` contiene:

- **Modelos de entrada (`AsteroideEntrada`):** Validan los datos que llegan en POST/PUT.
- **Modelos de salida (`AsteroideSalida`):** Definen la estructura de la respuesta.
- **Endpoints CRUD completos:** GET (listar y obtener uno), POST (crear), PUT (actualizar), DELETE (eliminar).
- **Manejo de errores:** `HTTPException` para devolver errores 404 cuando un recurso no existe.

---

## 2. Explicación de la clase / conceptos clave

### Pydantic BaseModel

Define esquemas de datos con validación automática:

```python
from pydantic import BaseModel, Field

class AsteroideEntrada(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    diametro_km: float = Field(..., gt=0)  # mayor que 0
    peligroso: bool = Field(default=False)
    fecha_acercamiento: date
```

Si el usuario envía un `diametro_km` negativo o un `nombre` de 2 caracteres, FastAPI devuelve automáticamente un error **422 Unprocessable Entity** con el detalle del problema.

### Campos comunes de Pydantic

| Campo | Descripción |
|-------|-------------|
| `Field(...)` | Campo obligatorio (los `...` significan requerido) |
| `Field(default=valor)` | Campo opcional con valor por defecto |
| `Field(min_length=n, max_length=n)` | Validar longitud de texto |
| `Field(gt=0)` | Validar que el número sea mayor a 0 |
| `Optional[Tipo]` | Campo que puede ser `None` |
| `EmailStr` | Validar que sea un correo electrónico válido |
| `List[Tipo]` | Lista de elementos de un tipo |

### `response_model`

Le decimos a FastAPI qué modelo usar para serializar la respuesta:

```python
@app.get("/asteroides", response_model=List[AsteroideSalida])
```

Esto asegura que solo se devuelvan los campos definidos en el modelo y que estén bien tipados.

### `HTTPException`

Para devolver errores personalizados con códigos HTTP específicos:

```python
raise HTTPException(status_code=404, detail="No encontrado")
```

---

## 3. Diccionario de sintaxis global - FastAPI + Pydantic

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

class Entrada(BaseModel):
    nombre: str = Field(..., min_length=3)
    edad: int = Field(..., gt=0, le=120)

@app.post("/datos", status_code=status.HTTP_201_CREATED)
def crear(datos: Entrada):
    return datos

@app.get("/dato/{id}")
def obtener(id: int):
    if id < 0:
        raise HTTPException(status_code=404, detail="No existe")
    return {"id": id}
```

---

## 4. Flujo de trabajo lógico

1. **Definir modelos de entrada:** ¿Qué datos espera la API? ¿Cuáles son obligatorios?
2. **Definir modelos de salida:** ¿Qué datos devuelve la API?
3. **Crear endpoints:** `@app.post()`, `@app.get()`, `@app.put()`, `@app.delete()`.
4. **Validar automáticamente:** FastAPI + Pydantic revisan los datos antes de ejecutar tu función.
5. **Manejar errores:** Usar `HTTPException` para casos como "no encontrado".

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| Error 422 | Datos de entrada no cumplen el modelo | Revisar el detalle del error y enviar los campos correctos |
| Error 404 | Recurso no existe | Verificar el ID antes de consultar o actualizar |
| Error 500 | Error interno del servidor | Revisar logs; envolver en try/except si es necesario |
| `response_model` no coincide | La respuesta tiene campos extra | Ajustar el modelo o filtrar la respuesta antes de retornar |

---

## 6. Adaptación a la competencia NSAC

Pydantic te protege de datos malformados que vengan de la API de la NASA o de otros integrantes del equipo. Define modelos claros para:

- Datos de asteroides (nombre, diámetro, fecha, peligroso).
- Datos de usuarios o reportes del equipo.
- Respuestas de tus propios endpoints.

Siguiente paso sugerido: `clase3_crud_con_bd` para conectar FastAPI con SQLite y hacer CRUD persistente.