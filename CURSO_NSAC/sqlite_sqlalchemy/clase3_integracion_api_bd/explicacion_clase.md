# Clase 3 - Integración: API de la NASA + pandas + SQLAlchemy

## 1. Explicación del ejemplo

Esta clase combina todo lo aprendido hasta ahora en un **flujo ETL** (Extraer, Transformar, Cargar):

1. **Extraer:** Consultar la API NeoWs de la NASA con `requests`.
2. **Transformar:** Aplanar el JSON anidado con `pd.json_normalize()` / `pandas` y limpiar los datos.
3. **Cargar:** Guardar los datos en SQLite con SQLAlchemy ORM, evitando duplicados.

Además, incluye una consulta de verificación para confirmar que los datos se guardaron correctamente.

---

## 2. Explicación de la clase / conceptos clave

### Flujo ETL completo

```
Extraer (requests)  →  Transformar (pandas)  →  Cargar (SQLAlchemy / SQLite)
     ↓                     ↓                        ↓
API de la NASA    JSON anidado → DataFrame   Tablas en SQLite
```

### Evitar duplicados

Antes de insertar, verificamos si ya existe un registro con el mismo nombre y fecha:

```python
existe = session.query(AsteroideNASA).filter(
    AsteroideNASA.nombre == fila["nombre"],
    AsteroideNASA.fecha_acercamiento == fila["fecha_acercamiento"]
).first()
```

Esto es fundamental para no llenar la base de datos con datos repetidos si ejecutas el flujo varias veces.

### Manejo de errores integrado

- Si la API falla → `try/except` con `requests.exceptions.RequestException`, retorna `None`.
- Si la base de datos falla → `session.rollback()` para deshacer cambios parciales.
- Si no hay datos → validamos `df.empty` antes de intentar cargar.

---

## 3. Diccionario de sintaxis global - Integración API + BD

```python
import requests
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Extraer
response = requests.get("https://api.nasa.gov/neo/rest/v1/feed", params=params, timeout=20)
datos = response.json()

# 2. Transformar
df = pd.json_normalize(lista_de_asteroides, sep="_")

# 3. Cargar
engine = create_engine("sqlite:///datos.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Evitar duplicados antes de insertar
if not session.query(Modelo).filter(Modelo.nombre == valor).first():
    session.add(Modelo(...))
    session.commit()

session.close()
```

---

## 4. Flujo de trabajo lógico para la competencia NSAC

1. **Definir qué datos necesitas:** ¿Asteroides? ¿Eventos naturales? ¿Fotos de Marte?
2. **Extraer:** Consultar la API con `requests` y `timeout`.
3. **Transformar:** `pandas` para aplanar JSON, filtrar, limpiar valores nulos.
4. **Cargar:** SQLite con SQLAlchemy, evitando duplicados.
5. **Consultar:** Leer de SQLite cuando necesites los datos, sin llamar otra vez a la API.
6. **Exponer:** (Próxima sección) FastAPI para que el equipo acceda a los datos mediante endpoints REST.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| API devuelve 429 | Límite de peticiones excedido | Esperar y reintentar; usar API key propia |
| `IntegrityError` | Registro duplicado | Verificar existencia antes de insertar |
| `ValueError` | Fecha en formato incorrecto | Usar `datetime.strptime(fecha, "%Y-%m-%d")` |
| Base de datos bloqueada | SQLite bloqueado por escritura concurrente | Cerrar sesiones correctamente; usar `check_same_thread=False` si es necesario |

---

## 6. Adaptación a la competencia NSAC

Este es el núcleo de tu trabajo en la hackathon:

- **Datos de la NASA** → **pandas** → **SQLite** → **FastAPI** (próxima sección).

Con este flujo, tu equipo tendrá una base de datos local siempre actualizada y una API propia para consultar los datos sin depender directamente de la NASA en cada petición.

Siguiente paso sugerido: `fastapi/clase1_endpoints_basicos` para aprender a exponer estos datos mediante una API REST propia.