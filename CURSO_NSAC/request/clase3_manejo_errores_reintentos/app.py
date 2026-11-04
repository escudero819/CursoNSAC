"""
Clase 3 - Manejo de errores y reintentos con requests

Objetivo:
- Aprender a no romper el programa cuando una API falla.
- Usar try/except para capturar excepciones de requests.
- Implementar reintentos (retry) con tiempo de espera exponencial.
- Detectar y manejar códigos de error HTTP (4xx, 5xx).
- Usar sesiones (requests.Session) para peticiones repetidas eficientes.

Requisitos:
- pip install requests
"""

import requests
import time


def peticion_con_try_except(url):
    """
    Ejemplo 1: Envolver la petición en try/except para capturar
    errores de conexión, timeout y respuesta inválida.
    """
    print("=" * 70)
    print("EJEMPLO 1: Petición con try/except")
    print("=" * 70)

    try:
        response = requests.get(url, timeout=5)

        # Verificamos errores HTTP (4xx, 5xx)
        # raise_for_status() lanza una excepción si status_code >= 400
        response.raise_for_status()

        datos = response.json()
        print(f"✓ Petición exitosa. Datos recibidos: {len(datos)} elementos")
        return datos

    except requests.exceptions.HTTPError as e:
        print(f"✗ Error HTTP: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Error de conexión: no se pudo alcanzar el servidor. {e}")
    except requests.exceptions.Timeout as e:
        print(f"✗ Tiempo de espera agotado (timeout). {e}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error genérico de requests: {e}")
    except ValueError as e:
        print(f"✗ Error al decodificar JSON: {e}")

    return None


def peticion_con_reintentos(url, max_reintentos=3, tiempo_espera=2):
    """
    Ejemplo 2: Reintentos con backoff exponencial.
    Si la API falla, esperamos y volvemos a intentar.
    Cada intento espera más tiempo que el anterior (2s, 4s, 8s...).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Petición con reintentos (backoff exponencial)")
    print("=" * 70)

    for intento in range(1, max_reintentos + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            print(f"✓ Éxito en el intento {intento}")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"✗ Intento {intento} falló: {e}")

            if intento < max_reintentos:
                espera = tiempo_espera * intento  # 2s, 4s, 6s...
                print(f"    Reintentando en {espera} segundos...")
                time.sleep(espera)
            else:
                print("    Se agotaron todos los reintentos.")

    return None


def usar_sesion_para_varias_peticiones(urls):
    """
    Ejemplo 3: Usar requests.Session para peticiones repetidas.
    Una sesión reusa la conexión TCP, lo que es más rápido y eficiente
    cuando haces muchas peticiones al mismo servidor (ej. NASA API).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Sesión reutilizable (requests.Session)")
    print("=" * 70)

    resultados = []

    # Creamos una sesión que se reusa para todas las peticiones
    with requests.Session() as sesion:
        # Podemos configurar cabeceras por defecto para toda la sesión
        sesion.headers.update({
            "User-Agent": "CursoNSAC/1.0 (Hackathon)",
            "Accept": "application/json"
        })

        for url in urls:
            try:
                response = sesion.get(url, timeout=10)
                response.raise_for_status()
                resultados.append(response.json())
                print(f"✓ {url} -> OK ({response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"✗ {url} -> Error: {e}")
                resultados.append(None)

    return resultados


if __name__ == "__main__":
    # URL que probablemente falle (dominio inexistente) para probar el manejo de errores
    url_mala = "https://dominio-inexistente-nasa-12345.com/datos"

    # URL que funciona bien
    url_buena = "https://jsonplaceholder.typicode.com/posts/1"

    print("Probando peticion con URL mala...")
    peticion_con_try_except(url_mala)

    print("\nProbando peticion con URL buena...")
    peticion_con_try_except(url_buena)

    print("\nProbando reintentos con URL mala (se reintentará 3 veces)...")
    peticion_con_reintentos(url_mala, max_reintentos=3, tiempo_espera=1)

    print("\nProbando sesión con múltiples URLs...")
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]
    usar_sesion_para_varias_peticiones(urls)