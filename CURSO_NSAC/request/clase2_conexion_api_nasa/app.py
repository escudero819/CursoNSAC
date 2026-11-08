"""
Clase 2 - Conexión a la API de la NASA con requests

Objetivo:
- Conectar con la API pública de la NASA (api.nasa.gov).
- Usar DEMO_KEY para pruebas sin registro.
- Manejar la autenticación mediante API key.
- Extraer y mostrar datos relevantes de la respuesta JSON (APOD y NeoWs).

Requisitos:
- pip install requests

Nota: La NASA ofrece una DEMO_KEY con límites bajos. Para la hackathon,
se recomienda registrar una API key gratuita en https://api.nasa.gov
"""

import requests
import json
from datetime import datetime, timedelta


NASA_BASE_URL = "https://api.nasa.gov"
API_KEY = "DEMO_KEY"  # Reemplaza por tu propia key de api.nasa.gov si tienes una


def obtener_apod():
    """
    Ejemplo 1: APOD (Astronomy Picture of the Day).
    Devuelve la imagen astronómica del día con título, explicación y URL.
    Endpoint: /planetary/apod
    """
    url = f"{NASA_BASE_URL}/planetary/apod"
    parametros = {
        "api_key": API_KEY
    }

    print("=" * 70)
    print("EJEMPLO 1: NASA APOD - Imagen astronómica del día")
    print("=" * 70)

    try:
        response = requests.get(url, params=parametros, timeout=15)

        if response.status_code == 200:
            datos = response.json()
            print(f"Título: {datos.get('title')}")
            print(f"Fecha: {datos.get('date')}")
            print(f"Explicación: {datos.get('explanation')[:200]}...")
            print(f"URL de la imagen: {datos.get('url')}")
            print(f"Tipo de medio: {datos.get('media_type')}")
        elif response.status_code == 403:
            print("✗ Error 403: API key inválida o límite excedido.")
        else:
            print(f"✗ Error {response.status_code}: {response.text[:200]}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")


def obtener_apod_fecha_especifica(fecha_str):
    """
    Ejemplo 2: APOD de una fecha específica.
    El parámetro 'date' permite consultar cualquier fecha pasada.
    """
    url = f"{NASA_BASE_URL}/planetary/apod"
    parametros = {
        "api_key": API_KEY,
        "date": fecha_str
    }

    print("\n" + "=" * 70)
    print(f"EJEMPLO 2: NASA APOD para la fecha {fecha_str}")
    print("=" * 70)

    try:
        response = requests.get(url, params=parametros, timeout=20)

        if response.status_code == 200:
            datos = response.json()
            print(f"✓ Fecha: {datos.get('date')}")
            print(f"✓ Título: {datos.get('title')}")
            print(f"✓ Explicación: {datos.get('explanation')[:150]}...")
        else:
            print(f"✗ No se pudo obtener la APOD. Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")


def obtener_asteroides_cercanos(fecha_inicio, fecha_fin):
    """
    Ejemplo 3: NeoWs (Near Earth Object Web Service).
    Consulta asteroides cercanos a la Tierra en un rango de fechas.
    Endpoint: /neo/rest/v1/feed
    """
    url = f"{NASA_BASE_URL}/neo/rest/v1/feed"
    parametros = {
        "api_key": API_KEY,
        "start_date": fecha_inicio,
        "end_date": fecha_fin
    }

    print("\n" + "=" * 70)
    print(f"EJEMPLO 3: NASA NeoWs - Asteroides cercanos ({fecha_inicio} a {fecha_fin})")
    print("=" * 70)

    try:
        response = requests.get(url, params=parametros, timeout=20)

        if response.status_code == 200:
            datos = response.json()
            conteo_total = datos.get("element_count", 0)
            print(f"✓ Total de asteroides encontrados: {conteo_total}")

            # Recorremos los asteroides por fecha
            cercanías_por_fecha = datos.get("near_earth_objects", {})
            for fecha, asteroides in cercanías_por_fecha.items():
                print(f"\n  Fecha {fecha}: {len(asteroides)} asteroide(s)")
                for ast in asteroides[:3]:  # Mostramos solo los primeros 3
                    nombre = ast.get("name", "Desconocido")
                    diametro_min = ast.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min", 0)
                    peligroso = ast.get("is_potentially_hazardous_asteroid", False)
                    print(f"    - {nombre} | Diámetro mín: {diametro_min:.2f} km | Peligroso: {peligroso}")
        else:
            print(f"✗ Error al consultar NeoWs. Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")


if __name__ == "__main__":
    # Ejemplo 1: APOD de hoy
    obtener_apod()

    # Ejemplo 2: APOD de una fecha histórica (ej. llegada a la Luna)
    obtener_apod_fecha_especifica("1969-07-20")

    # Ejemplo 3: Asteroides cercanos en los últimos 7 días
    hoy = datetime.now().date()
    hace_siete_dias = hoy - timedelta(days=7)
    obtener_asteroides_cercanos(str(hace_siete_dias), str(hoy))