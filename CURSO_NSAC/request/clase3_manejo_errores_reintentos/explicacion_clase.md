# Clase 3 - Manejo de errores y reintentos con `requests`

## 1. Explicación del ejemplo

En una hackathon, las APIs externas pueden caer, tardar demasiado o devolver errores. Si tu programa no maneja estos fallos, se detendrá en medio de la competencia y perderás tiempo valioso.

Esta clase enseña a **blindar tus peticiones HTTP** con tres técnicas:

1. **try/except:** Captura errores de conexión, timeout, respuesta HTTP inválida y JSON mal formado.
2. **Reintentos con backoff exponencial:** Si la petición falla, espera y vuelve a intentar, aumentando el tiempo de espera en cada intento (2s, 4s, 6s...).
3. **requests.Session:** Reusa la conexión TCP para múltiples peticiones al mismo servidor, lo que es más rápido y eficiente.

---

## 2. Explicación de la clase / conceptos clave

### Excepciones de `requests`

| Excepción | Cuándo ocurre |
|-----------|---------------|
| `requests.exceptions.HTTPError` | Código de estado 4xx o 5xx (lanzado por `raise_for_status()`) |
| `requests.exceptions.ConnectionError` | No se pudo conectar al servidor (DNS, red caída) |
| `requests.exceptions.Timeout` | La petición tardó más que el `timeout` definido |
| `requests.exceptions.RequestException` | Clase base de todas las excepciones de requests |

### `raise_for_status()`

Este método lanza una excepción automáticamente si `response.status_code` es 400 o superior. Es la forma más limpia de detectar errores HTTP sin escribir `if response.status_code != 200:` en cada petición.

### Retry con backoff exponencial

En lugar de reintentar inmediatamente (lo que podría saturar más el servidor), esperamos un tiempo que crece en cada intento:

- Intento 1: falla → esperar 2s
- Intento 2: falla → esperar 4s
- Intento 3: falla → esperar 6s (o 8s si usas multiplicación)

> **Tip de la hackathon:** No abuses de los reintentos. 3 intentos es generalmente suficiente. Si fallan los 3, pasa a un plan B (usar datos en caché, mostrar aviso al usuario, etc.).

### `requests.Session`

Cuando haces varias peticiones al mismo servidor (por ejemplo, consultar varios asteroides de la NASA), usar una sesión reusa la conexión TCP y evita el overhead de establecer una nueva conexión cada vez.

---

## 3. Diccionario de sintaxis global - manejo de errores

```python
import requests
import time

# Petición segura con try/except
try:
    response = requests.get("https://api.ejemplo.com/datos", timeout=10)
    response.raise_for_status()  # Lanza excepción si hay error HTTP
    datos = response.json()
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"Error de conexión: {e}")
except requests.exceptions.Timeout as e:
    print(f"Timeout: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error genérico: {e}")

# Reintento simple con backoff
max_reintentos = 3
for intento in range(1, max_reintentos + 1):
    try:
        response = requests.get("https://api.ejemplo.com/datos", timeout=10)
        response.raise_for_status()
        break  # Salimos si tuvo éxito
    except requests.exceptions.RequestException:
        if intento == max_reintentos:
            raise
        time.sleep(2 * intento)

# Sesión reutilizable
with requests.Session() as sesion:
    sesion.headers.update({"Authorization": "Bearer TU_TOKEN"})
    r1 = sesion.get("https://api.ejemplo.com/datos/1")
    r2 = sesion.get("https://api.ejemplo.com/datos/2")
```

---

## 4. Flujo de trabajo lógico (razonamiento de un data scientist)

1. **Suponer que la API puede fallar:** Nunca confíes ciegamente en una respuesta externa.
2. **Definir cuántos reintentos son aceptables:** En una hackathon, 2-3 intentos es lo razonable.
3. **Decidir un plan B:** Si los reintentos fallan, ¿usas datos locales guardados? ¿avisas al equipo? ¿saltas ese dato?
4. **Registrar los errores:** Imprime o guarda qué falló para poder debuguear rápido bajo presión.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `ConnectionError` | Sin internet o servidor caído | Verificar conexión; usar datos en caché si existen |
| `Timeout` | API lenta | Aumentar `timeout`; implementar reintentos |
| `HTTPError 429` | Límite de peticiones excedido | Esperar más tiempo entre reintentos; usar tu propia API key |
| `HTTPError 500` | Error interno del servidor de la API | Reintentar después de unos segundos; no es culpa de tu código |
| `JSONDecodeError` | La respuesta no es JSON válido | Revisar `response.text`; puede ser una página de error HTML |

---

## 6. Adaptación a la competencia NSAC

Durante la hackathon, la API de la NASA puede estar lenta o caerse por el tráfico de muchos equipos. Con lo aprendido en esta clase:

- Tu programa no se congelará si la NASA tarda en responder (gracias a `timeout`).
- No se detendrá por un error puntual (gracias a `try/except`).
- Se recuperará solo en muchos casos (gracias a los reintentos).

Siguiente paso sugerido: pasar a `pandas/clase1_estructuras_datos` para aprender a procesar los JSON que recibes de las APIs.