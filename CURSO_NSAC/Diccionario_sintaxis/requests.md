# Diccionario de sintaxis rápida - `requests`

## Instalación
```bash
pip install requests
```

## Importación
```python
import requests
```

## Peticiones HTTP

| Operación | Sintaxis |
|-----------|----------|
| GET simple | `response = requests.get("https://api.ejemplo.com/datos", timeout=10)` |
| GET con parámetros | `response = requests.get(url, params={"clave": "valor"}, timeout=10)` |
| POST enviando JSON | `response = requests.post(url, json={"campo": "valor"}, timeout=10)` |
| PUT | `response = requests.put(url, json=datos, timeout=10)` |
| DELETE | `response = requests.delete(url, timeout=10)` |
| Con cabeceras | `response = requests.get(url, headers={"Authorization": "Bearer TOKEN"}, timeout=10)` |

## Respuesta (`response`)

| Atributo / Método | Qué devuelve | Uso |
|-------------------|--------------|-----|
| `response.status_code` | Código HTTP (200, 404, 500...) | Verificar si tuvo éxito |
| `response.json()` | Diccionario o lista de Python | Leer cuerpo como JSON |
| `response.text` | Texto plano | Leer cuerpo como string |
| `response.url` | URL final | Ver URL después de parámetros/redirecciones |
| `response.headers` | Diccionario | Cabeceras de la respuesta |
| `response.ok` | Booleano | `True` si status_code < 400 |

## Manejo de errores

```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Lanza excepción si status >= 400
    datos = response.json()
except requests.exceptions.HTTPError as e:
    print("Error HTTP:", e)
except requests.exceptions.ConnectionError as e:
    print("Error de conexión:", e)
except requests.exceptions.Timeout as e:
    print("Tiempo agotado:", e)
except requests.exceptions.RequestException as e:
    print("Error genérico:", e)
```

## Sesión reutilizable (varias peticiones al mismo servidor)

```python
with requests.Session() as sesion:
    sesion.headers.update({"User-Agent": "CursoNSAC/1.0"})
    r1 = sesion.get("https://api.ejemplo.com/datos/1")
    r2 = sesion.get("https://api.ejemplo.com/datos/2")
```

## Reintento simple con backoff

```python
import time
max_reintentos = 3
for intento in range(1, max_reintentos + 1):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        break
    except requests.exceptions.RequestException:
        if intento == max_reintentos:
            raise
        time.sleep(2 * intento)
```

## API de la NASA (ejemplo)

```python
BASE_URL = "https://api.nasa.gov"
API_KEY = "TU_API_KEY"

params = {"api_key": API_KEY, "date": "2026-11-01"}
response = requests.get(f"{BASE_URL}/planetary/apod", params=params, timeout=15)
```

---

> **Tip:** Siempre usa `timeout` en tus peticiones para que el programa no se quede esperando indefinidamente.