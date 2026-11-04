# Clase 2 - Conexión a la API de la NASA con `requests`

## 1. Explicación del ejemplo

Esta clase enseña a conectar específicamente con la **API pública de la NASA** (`https://api.nasa.gov`), que es la fuente de datos principal que usarán en la hackathon NSAC.

El archivo `app.py` contiene tres ejemplos:

1. **APOD (Astronomy Picture of the Day):** Obtiene la imagen astronómica del día con su título, explicación y URL. Es el endpoint más simple y no requiere parámetros complejos.
2. **APOD con fecha específica:** Muestra cómo consultar cualquier fecha pasada usando el parámetro `date`. Útil para comparar eventos históricos.
3. **NeoWs (Near Earth Object Web Service):** Consulta asteroides cercanos a la Tierra en un rango de fechas. Es un ejemplo más avanzado porque la respuesta está **anidada** (diccionarios dentro de diccionarios y listas).

---

## 2. Explicación de la clase / conceptos clave

### API Key de la NASA

La mayoría de los endpoints de la NASA requieren un parámetro `api_key`. Para pruebas rápidas puedes usar `DEMO_KEY`, pero tiene límites bajos de peticiones por hora.

**Recomendación para la hackathon:** Regístrate en https://api.nasa.gov y obtén tu propia API key gratuita. Guárdala en una variable de entorno o un archivo de configuración, nunca la subas a GitHub pública.

### Endpoints útiles de la NASA para la hackathon

| Endpoint | Descripción | Parámetros clave |
|----------|-------------|------------------|
| `/planetary/apod` | Imagen astronómica del día | `date`, `api_key` |
| `/neo/rest/v1/feed` | Asteroides cercanos a la Tierra | `start_date`, `end_date`, `api_key` |
| `/EONET/v2.1/events` | Eventos naturales (volcanes, incendios, tormentas) | `status`, `limit`, `api_key` |
| `/mars-photos/api/v1/rovers/{rover}/photos` | Fotos de los rovers de Marte | `sol`, `camera`, `api_key` |

### Estructura de respuesta anidada (NeoWs)

La respuesta de NeoWs tiene este esquema simplificado:

```json
{
  "element_count": 45,
  "near_earth_objects": {
    "2026-11-01": [
      {
        "name": "(2026 XY1)",
        "estimated_diameter": {
          "kilometers": {
            "estimated_diameter_min": 0.012,
            "estimated_diameter_max": 0.027
          }
        },
        "is_potentially_hazardous_asteroid": false
      }
    ]
  }
}
```

Para acceder a datos anidados en Python, usa encadenamiento seguro con `.get()` para evitar `KeyError`:

```python
diametro = datos.get("near_earth_objects", {}).get("2026-11-01", [])[0].get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min", 0)
```

---

## 3. Diccionario de sintaxis global - `requests` con API de la NASA

```python
import requests

BASE_URL = "https://api.nasa.gov"
API_KEY = "TU_API_KEY_AQUI"

# Parámetros como diccionario
params = {
    "api_key": API_KEY,
    "date": "2026-11-01",
    "start_date": "2026-10-25",
    "end_date": "2026-11-01"
}

# Petición GET
response = requests.get(f"{BASE_URL}/planetary/apod", params=params, timeout=15)

# Verificar éxito y parsear JSON
if response.status_code == 200:
    datos = response.json()
else:
    print(f"Error {response.status_code}")
```

---

## 4. Flujo de trabajo lógico

1. **Elegir el endpoint:** Según el dato que necesites (imagen, asteroide, evento natural, foto de Marte).
2. **Armar los parámetros:** Incluye siempre `api_key` y los filtros de fecha necesarios.
3. **Hacer la petición:** `requests.get()` con `timeout`.
4. **Validar estado:** `200` = éxito; `403` = problema con la key; `429` = límite excedido.
5. **Extraer datos anidados:** Usar `.get()` con valores por defecto para no romper el programa si falta una clave.
6. **Guardar o transformar:** Los datos pasan a `pandas` (clase siguiente) o a SQLite.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `403 Forbidden` | API key inválida o DEMO_KEY agotado | Registrar key propia en api.nasa.gov |
| `429 Too Many Requests` | Demasiadas peticiones en poco tiempo | Esperar un minuto y reintentar; usar `time.sleep()` |
| `KeyError` | Se accede a una clave que no existe en el JSON anidado | Usar siempre `.get("clave", valor_por_defecto)` |
| `404` | Endpoint no existe o fecha inválida | Verificar la URL y el formato de fecha `YYYY-MM-DD` |

---

## 6. Adaptación a la competencia NSAC

En la hackathon probablemente necesitarás combinar varios endpoints de la NASA. El patrón es siempre el mismo:

1. Armar la URL base + endpoint.
2. Agregar `api_key`.
3. Consultar y validar.
4. Pasar el JSON a `pandas` para limpiarlo.
5. Guardar lo relevante en SQLite.

Siguiente paso sugerido: `clase3_manejo_errores_reintentos` para aprender a no romper tu programa cuando la API falle en medio de la competencia.