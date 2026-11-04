# Clase 4 - FastAPI: Integración con la API de la NASA

## 1. Explicación del ejemplo

Esta clase combina todo el curso: consumes la **API de la NASA** (EONET - eventos naturales como volcanes, incendios, tormentas), guardas los datos en **SQLite** local y los expones mediante endpoints de **FastAPI**.

El archivo `app.py` contiene:

1. **GET /eventos** → Lista eventos guardados localmente (con filtro por fuente y límite).
2. **POST /sincronizar-nasa** → Consulta la API de la NASA y guarda los eventos en SQLite (evita duplicados).
3. **GET /eventos/{id}** → Obtiene un evento específico.
4. **DELETE /eventos/{id}** → Elimina un evento.

Además usa **`BackgroundTasks`** para que la sincronización no bloquee la respuesta HTTP.

---

## 2. Explicación de la clase / conceptos clave

### ¿Por qué guardar datos de la NASA en SQLite local?

- **Rate limit:** La NASA limita cuántas peticiones puedes hacer por hora. Guardar localmente evita llegar al límite.
- **Disponibilidad:** Si la API de la NASA cae, tu equipo sigue consultando los datos desde tu BD local.
- **Velocidad:** Consultar SQLite local es mucho más rápido que hacer una petición HTTP externa.

### `BackgroundTasks`

Permite ejecutar una tarea en segundo plano después de enviar la respuesta HTTP. Ideal para operaciones lentas como sincronizar con una API externa:

```python
@app.post("/sincronizar-nasa")
def sincronizar(background_tasks: BackgroundTasks, ...):
    background_tasks.add_task(tarea_lenta)
    return {"mensaje": "Sincronizacion iniciada"}
```

### Evitar duplicados al sincronizar

Antes de insertar, verificamos si ya existe un evento con el mismo título y fecha:

```python
existe = db.query(EventoNasaDB).filter(
    EventoNasaDB.titulo == titulo,
    EventoNasaDB.fecha_evento == fecha_evento
).first()
```

---

## 3. Diccionario de sintaxis global - Integración NASA + FastAPI

```python
import requests
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/sincronizar")
def sincronizar(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(tarea_de_sincronizacion, db)
    return {"mensaje": "Sincronizando en segundo plano"}

def tarea_de_sincronizacion(db: Session):
    response = requests.get("https://api.nasa.gov/EONET/v2.1/events", params={"api_key": KEY})
    datos = response.json()
    # Guardar en db...
```

---

## 4. Flujo de trabajo lógico para la competencia NSAC

1. **Identificar la fuente de datos NASA** (EONET, NeoWs, APOD, etc.).
2. **Crear endpoint de sincronización:** Consulta la API y guarda en SQLite.
3. **Crear endpoints de consulta:** Lee desde SQLite local (rápido y sin depender de internet).
4. **Programar sincronización periódica:** O sincronizar manualmente antes de presentar.
5. **Documentar en `/docs`:** Para que el equipo sepa qué endpoints existen.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| API de la NASA no responde | Sin internet o servidor caído | `try/except` + `HTTPException 503`; usar datos locales guardados |
| Error 429 | Límite de peticiones excedido | Esperar; usar API key propia; no sincronizar muy seguido |
| Fecha inválida | Formato de fecha inesperado | `try/except` al convertir con `datetime.strptime()` |
| Duplicados | Ejecutar sincronización varias veces | Verificar existencia antes de insertar |

---

## 6. Adaptación a la competencia NSAC

Este es el endpoint central de tu proyecto:

- Tu equipo consulta `/eventos` para ver datos sin llamar a la NASA directamente.
- Usas `/sincronizar-nasa` antes de la presentación para tener datos frescos.
- Combina con la clase anterior (CRUD) para agregar registros personalizados del equipo.

> **Has completado todo el curso.** Ahora sabes consultar APIs (`requests`), procesar datos (`pandas`), guardar en SQLite (`SQLAlchemy`) y exponer todo mediante FastAPI. ¡Éxito en la hackathon NSAC!