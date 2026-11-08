# Ejercicios Prácticos - Clase 1: Endpoints básicos con FastAPI

## Objetivo
Crear una API REST mínima con FastAPI, definir endpoints GET con parámetros de ruta y de consulta, ejecutar el servidor y probar los endpoints desde el navegador o con curl.

## Qué hay que hacer

1. **Crear la aplicación:** Instancia un objeto `FastAPI()` y define al menos tres endpoints GET:
   - Un endpoint raíz (`/`) que devuelva un mensaje de bienvenida.
   - Un endpoint que liste una colección de datos en memoria (por ejemplo, una lista de asteroides o eventos espaciales).
   - Un endpoint que devuelva un solo elemento por su ID usando un parámetro de ruta (`/elemento/{id}`).

2. **Parámetro de ruta:** El endpoint por ID debe aceptar un parámetro de ruta de tipo entero (`int`) y devolver el elemento que coincida con ese ID. Si no se encuentra, devolver un mensaje de error en JSON (por ejemplo, `{"error": "No encontrado"}`).

3. **Parámetros de consulta:** Crea un endpoint de búsqueda (`/buscar`) que acepte al menos dos parámetros de consulta opcionales (por ejemplo, `nombre` y `peligroso`). Filtre los datos en memoria según los parámetros recibidos y devuelva los resultados filtrados.

4. **Ejecutar el servidor:** Levanta el servidor con `uvicorn app:app --reload` y verifica que se inicie sin errores en el puerto 8000.

5. **Probar los endpoints:** Abre en el navegador o usa curl para probar:
   - `http://127.0.0.1:8000/`
   - `http://127.0.0.1:8000/coleccion` (o el nombre que elijas para listar)
   - `http://127.0.0.1:8000/coleccion/1`
   - `http://127.0.0.1:8000/coleccion/999` (un ID que no exista, para probar el error)
   - `http://127.0.0.1:8000/buscar?nombre=texto&peligroso=true`

6. **Documentación automática:** Abre `http://127.0.0.1:8000/docs` y verifica que FastAPI generó la documentación interactiva (Swagger UI) con todos tus endpoints listados.

## Resultado esperado

- Un archivo `app.py` que ejecute una API FastAPI con al menos 3 endpoints GET.
- El servidor levantado y accesible en `http://127.0.0.1:8000`.
- Respuestas JSON correctas para cada endpoint probado.
- El endpoint por ID devuelve el elemento correcto cuando existe y un mensaje de error cuando no existe.
- El endpoint de búsqueda filtra correctamente según los parámetros de consulta enviados.
- La página `/docs` muestra todos los endpoints disponibles para probar desde la interfaz web.

## Pistas

- Usa `@app.get("/ruta")` sobre una función para definir cada endpoint.
- Los parámetros de ruta se definen en la URL entre llaves: `/elemento/{elemento_id}` y en la función como `elemento_id: int`.
- Los parámetros de consulta se definen como argumentos opcionales de la función: `nombre: Optional[str] = None`.
- FastAPI convierte automáticamente los valores de retorno (diccionarios, listas) a JSON.
- Usa `--reload` en uvicorn para que el servidor se reinicie solo al guardar cambios.

## Dificultad

Principiante

---