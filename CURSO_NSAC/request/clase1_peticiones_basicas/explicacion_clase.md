# Clase 1 - Peticiones HTTP básicas con `requests`

## 1. Explicación del ejemplo

En esta clase aprendes a hacer peticiones HTTP desde Python usando la librería **`requests`**, que es el estándar de facto para consumir APIs REST en Python.

El archivo `app.py` contiene cuatro ejemplos progresivos:

1. **GET simple:** Obtiene un recurso único de una API pública.
2. **GET con parámetros:** Filtra resultados enviando parámetros en la URL (`?userId=1&_limit=3`).
3. **POST:** Envía datos al servidor en formato JSON (útil para crear registros).
4. **Con cabeceras:** Envía metadatos en la petición (tipo de contenido, agente de usuario, autenticación).

> **Tip de la hackathon:** Siempre usa `timeout=10` (o un valor razonable) en tus peticiones. Si la API tarda demasiado, tu programa no se quedará colgado esperando para siempre.

---

## 2. Explicación de la clase `requests`

La librería `requests` abstrae la complejidad de las peticiones HTTP. Sus funciones principales son:

| Función | Uso típico |
|---------|------------|
| `requests.get(url, ...)` | Obtener datos de un recurso |
| `requests.post(url, json={...}, ...)` | Enviar datos para crear un recurso |
| `requests.put(url, json={...}, ...)` | Actualizar un recurso existente |
| `requests.delete(url, ...)` | Eliminar un recurso |

### Atributos importantes del objeto `response`

| Atributo | Qué devuelve | Para qué sirve |
|----------|--------------|----------------|
| `response.status_code` | Código HTTP (200, 404, 500, etc.) | Saber si la petición tuvo éxito |
| `response.json()` | Diccionario / lista de Python | Leer el cuerpo de la respuesta como JSON |
| `response.text` | Texto plano | Leer la respuesta como string |
| `response.url` | URL final | Ver la URL después de agregar parámetros o redirecciones |
| `response.headers` | Diccionario de cabeceras | Ver metadatos de la respuesta (Content-Type, etc.) |

---

## 3. Diccionario de sintaxis global - `requests` (clase 1)

```python
import requests

# GET simple
response = requests.get("https://api.ejemplo.com/datos", timeout=10)

# GET con parámetros de consulta
params = {"clave1": "valor1", "clave2": "valor2"}
response = requests.get("https://api.ejemplo.com/datos", params=params, timeout=10)

# POST enviando JSON
datos = {"nombre": "Ana", "edad": 25}
response = requests.post("https://api.ejemplo.com/datos", json=datos, timeout=10)

# Con cabeceras personalizadas
headers = {"Authorization": "Bearer TOKEN_AQUI", "Accept": "application/json"}
response = requests.get("https://api.ejemplo.com/privado", headers=headers, timeout=10)

# Leer la respuesta
if response.status_code == 200:
    datos = response.json()
    print(response.text)
```

---

## 4. Flujo de trabajo lógico (razonamiento de un data scientist)

1. **Definir el endpoint:** ¿Qué URL debo consultar? ¿Qué datos necesito?
2. **Hacer la petición:** Usar `requests.get()` o `requests.post()`.
3. **Validar la respuesta:** Revisar `response.status_code`. Si no es 200, algo falló.
4. **Extraer los datos:** Usar `response.json()` para convertirlos a estructuras de Python.
5. **Manejar errores:** Envolver en `try/except` para no romper el programa si la caída de la red o la API.

---

## 5. Posibles errores y cómo solucionarlos

| Error | Causa probable | Solución |
|-------|----------------|----------|
| `ConnectionError` | No hay internet o la URL está mal | Verificar conexión y URL |
| `Timeout` | La API tardó demasiado en responder | Aumentar `timeout` o reintentar |
| `404 Not Found` | El recurso no existe | Revisar la URL del endpoint |
| `401 Unauthorized` | Falta autenticación o token inválido | Agregar cabecera `Authorization` correcta |
| `429 Too Many Requests` | Excediste el límite de peticiones (rate limit) | Esperar y reintentar con backoff |
| `JSONDecodeError` | La respuesta no es JSON válido | Revisar `response.text` antes de hacer `.json()` |

---

## 6. Cómo adaptar esto a la competencia NSAC

Durante la hackathon probablemente consumirás la API de la NASA. El patrón es exactamente el mismo que en esta clase, solo cambia la URL y posiblemente necesites una `API_KEY` en las cabeceras o como parámetro de consulta.

Siguiente paso sugerido: ve a `clase2_conexion_api_nasa` para ver cómo conectar específicamente con la API de la NASA.