"""
Clase 1 - Peticiones HTTP basicas con la librería requests

Objetivo:
- Entender qué es una petición HTTP (GET y POST).
- Aprender a consumir una API pública y leer su respuesta.
- Conocer los códigos de estado HTTP más comunes.
- Manejar cabeceras (headers) y parámetros de consulta (query params).

Este archivo es ejecutable de forma independiente.
"""

import requests
import json


def peticion_get_simple():
    """
    Ejemplo 1: Petición GET simple a una API pública de prueba.
    Usamos https://jsonplaceholder.typicode.com que devuelve datos falsos
    pero con estructura real, ideal para practicar sin depender de la NASA.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1"

    print("=" * 60)
    print("EJEMPLO 1: Petición GET simple")
    print("=" * 60)

    try:
        # requests.get(url) realiza una petición HTTP GET
        response = requests.get(url, timeout=10)

        # Verificamos si la petición fue exitosa (código 200)
        if response.status_code == 200:
            datos = response.json()  # Convertimos la respuesta a diccionario Python
            print("✓ Petición exitosa (status 200)")
            print(f"Título del post: {datos.get('title')}")
            print(f"Cuerpo: {datos.get('body')[:80]}...")
        else:
            print(f"✗ Error en la petición. Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Ocurrió un error de conexión: {e}")


def peticion_get_con_parametros():
    """
    Ejemplo 2: Petición GET con parámetros de consulta (query params).
    Los query params se pasan como un diccionario en el argumento 'params'.
    """
    url = "https://jsonplaceholder.typicode.com/posts"

    print("\n" + "=" * 60)
    print("EJEMPLO 2: GET con parámetros de consulta")
    print("=" * 60)

    # Diccionario de parámetros que se agregarán a la URL
    # Ejemplo: /posts?userId=1&_limit=3
    parametros = {
        "userId": 1,
        "_limit": 3
    }

    try:
        response = requests.get(url, params=parametros, timeout=10)

        print(f"URL final generada: {response.url}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            lista_posts = response.json()
            print(f"Se recibieron {len(lista_posts)} posts del usuario 1:")
            for post in lista_posts:
                print(f"  - ID {post['id']}: {post['title']}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")


def peticion_post():
    """
    Ejemplo 3: Petición POST para enviar datos a un servidor.
    Se envía un cuerpo JSON en el argumento 'json'.
    """
    url = "https://jsonplaceholder.typicode.com/posts"

    print("\n" + "=" * 60)
    print("EJEMPLO 3: Petición POST enviando datos JSON")
    print("=" * 60)

    # Datos que queremos enviar (simulamos un nuevo registro)
    nuevo_registro = {
        "title": "Registro NSAC Hackathon",
        "body": "Datos recolectados de la API de la NASA para la competencia",
        "userId": 1
    }

    try:
        response = requests.post(url, json=nuevo_registro, timeout=10)

        print(f"Status: {response.status_code}")
        if response.status_code in (200, 201):
            datos_creados = response.json()
            print("✓ Registro creado con éxito:")
            print(json.dumps(datos_creados, indent=2, ensure_ascii=False))
        else:
            print(f"✗ No se pudo crear el registro. Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")


def peticion_con_cabeceras():
    """
    Ejemplo 4: Petición GET enviando cabeceras personalizadas (headers).
    Algunas APIs requieren autenticación o especifican el tipo de contenido.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1"

    print("\n" + "=" * 60)
    print("EJEMPLO 4: Petición con cabeceras personalizadas")
    print("=" * 60)

    # Cabeceras comunes: User-Agent, Accept, Authorization
    cabeceras = {
        "User-Agent": "CursoNSAC/1.0 (Hackathon NASA Space Apps)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=cabeceras, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Cabecera Content-Type del servidor: {response.headers.get('Content-Type')}")

        if response.status_code == 200:
            print("✓ Respuesta recibida con cabeceras personalizadas")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    peticion_get_simple()
    peticion_get_con_parametros()
    peticion_post()
    peticion_con_cabeceras()