# Clase 1 - FastAPI: Endpoints basicos
# Objetivo:
# - Crear una API REST minima con FastAPI.
# - Definir endpoints GET con parametros de ruta (path params) y de consulta (query params).
# - Ejecutar el servidor con uvicorn.
# - Probar los endpoints con el navegador o curl.
#
# Requisitos:
#   pip install fastapi uvicorn
#
# Como ejecutar:
#   uvicorn app:app --reload
#
# Luego abre en el navegador:
#   http://127.0.0.1:8000/
#   http://127.0.0.1:8000/asteroides
#   http://127.0.0.1:8000/asteroide/1
#   http://127.0.0.1:8000/buscar?nombre=Marte

from fastapi import FastAPI
from typing import Optional

app = FastAPI(title="API NSAC - Datos de la NASA", version="1.0.0")

# Datos en memoria (simulando una base de datos)
asteroides_db = [
    {"id": 1, "nombre": "(2026 AB1)", "diametro_km": 0.15, "peligroso": False},
    {"id": 2, "nombre": "(2026 CD2)", "diametro_km": 0.42, "peligroso": True},
    {"id": 3, "nombre": "(2026 EF3)", "diametro_km": 0.08, "peligroso": False},
]


@app.get("/")
def raiz():
    # Endpoint raiz. Devuelve un mensaje de bienvenida.
    return {"mensaje": "Bienvenido a la API NSAC - Datos espaciales de la NASA"}


@app.get("/asteroides")
def listar_asteroides():
    # Devuelve la lista completa de asteroides.
    return {"total": len(asteroides_db), "asteroides": asteroides_db}


@app.get("/asteroide/{asteroide_id}")
def obtener_asteroide(asteroide_id: int):
    # Endpoint con parametro de ruta (path parameter).
    # Devuelve un asteroide segun su ID.
    for ast in asteroides_db:
        if ast["id"] == asteroide_id:
            return ast
    return {"error": "No se encontro asteroide con ID " + str(asteroide_id)}


@app.get("/buscar")
def buscar_asteroide(nombre: Optional[str] = None, peligroso: Optional[bool] = None):
    # Endpoint con parametros de consulta (query parameters).
    # Ejemplo: /buscar?nombre=2026&peligroso=true
    resultados = asteroides_db

    if nombre:
        resultados = [a for a in resultados if nombre.lower() in a["nombre"].lower()]

    if peligroso is not None:
        resultados = [a for a in resultados if a["peligroso"] == peligroso]

    return {"total": len(resultados), "resultados": resultados}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)