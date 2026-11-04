# Clase 2 - FastAPI: Modelos Pydantic (validacion de datos)
# Objetivo:
# - Definir modelos de entrada y salida con Pydantic (BaseModel).
# - Validar datos que llegan en peticiones POST/PUT.
# - Retornar respuestas tipadas y documentadas automaticamente.
# - Manejar errores de validacion de forma amigable.
#
# Requisitos:
#   pip install fastapi uvicorn
#
# Como ejecutar:
#   uvicorn app:app --reload
#
# Documentacion:
#   http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date


app = FastAPI(title="API NSAC - Modelos Pydantic", version="1.0.0")

# Base de datos en memoria (simulada)
registro_db = []
contador_id = 1


# --- Modelos Pydantic ---

class AsteroideEntrada(BaseModel):
    # Modelo para validar datos que entran (entrada de datos).
    # Se usa en peticiones POST y PUT.
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del asteroide")
    diametro_km: float = Field(..., gt=0, description="Diametro en kilometros (debe ser > 0)")
    peligroso: bool = Field(default=False, description="Es potencialmente peligroso")
    fecha_acercamiento: date = Field(..., description="Fecha de acercamiento (YYYY-MM-DD)")
    email_contacto: Optional[EmailStr] = Field(None, description="Email de contacto opcional")


class AsteroideSalida(BaseModel):
    # Modelo para validar datos que salen (respuesta).
    # Incluye el ID asignado por el sistema.
    id: int
    nombre: str
    diametro_km: float
    peligroso: bool
    fecha_acercamiento: date


class MensajeRespuesta(BaseModel):
    mensaje: str
    exito: bool


# --- Endpoints ---

@app.get("/")
def raiz():
    return {"mensaje": "API con validacion Pydantic activa"}


@app.get("/asteroides", response_model=List[AsteroideSalida])
def listar_asteroides():
    # Devuelve la lista de asteroides validada por el modelo de salida.
    return registro_db


@app.post("/asteroides", response_model=AsteroideSalida, status_code=status.HTTP_201_CREATED)
def crear_asteroide(datos: AsteroideEntrada):
    # Crea un nuevo asteroide.
    # FastAPI valida automaticamente que 'datos' cumpla con AsteroideEntrada.
    # Si no, devuelve error 422 con detalle de los campos invalidos.
    global contador_id
    nuevo = {
        "id": contador_id,
        "nombre": datos.nombre,
        "diametro_km": datos.diametro_km,
        "peligroso": datos.peligroso,
        "fecha_acercamiento": datos.fecha_acercamiento
    }
    registro_db.append(nuevo)
    contador_id += 1
    return nuevo


@app.get("/asteroide/{asteroide_id}", response_model=AsteroideSalida)
def obtener_asteroide(asteroide_id: int):
    # Obtiene un asteroide por ID.
    # Si no existe, devuelve error 404 personalizado.
    for ast in registro_db:
        if ast["id"] == asteroide_id:
            return ast
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Asteroide con ID " + str(asteroide_id) + " no encontrado"
    )


@app.put("/asteroide/{asteroide_id}", response_model=AsteroideSalida)
def actualizar_asteroide(asteroide_id: int, datos: AsteroideEntrada):
    # Actualiza un asteroide existente.
    # Valida tanto el ID de la ruta como los datos de entrada.
    for ast in registro_db:
        if ast["id"] == asteroide_id:
            ast["nombre"] = datos.nombre
            ast["diametro_km"] = datos.diametro_km
            ast["peligroso"] = datos.peligroso
            ast["fecha_acercamiento"] = datos.fecha_acercamiento
            return ast
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Asteroide con ID " + str(asteroide_id) + " no encontrado para actualizar"
    )


@app.delete("/asteroide/{asteroide_id}", response_model=MensajeRespuesta)
def eliminar_asteroide(asteroide_id: int):
    # Elimina un asteroide por ID.
    global registro_db
    for i, ast in enumerate(registro_db):
        if ast["id"] == asteroide_id:
            registro_db.pop(i)
            return {"mensaje": "Asteroide " + str(asteroide_id) + " eliminado", "exito": True}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Asteroide con ID " + str(asteroide_id) + " no encontrado para eliminar"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)