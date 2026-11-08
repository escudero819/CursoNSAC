# Ejercicios Prácticos - Clase 2: Modelos Pydantic con FastAPI

## Objetivo
Validar datos de entrada y salida usando Pydantic (`BaseModel`), definir campos obligatorios y opcionales con restricciones, manejar errores de validación y usar `HTTPException` para respuestas personalizadas.

## Qué hay que hacer

1. **Definir un modelo de entrada:** Crea una clase `RegistroEntrada` que herede de `BaseModel` con al menos estos campos:
   - `nombre`: string obligatorio, con longitud mínima 3 y máxima 100.
   - `valor`: número decimal obligatorio, mayor que 0.
   - `activo`: booleano opcional con valor por defecto `False`.
   - `fecha`: fecha obligatoria.
   - `email`: string opcional que valide formato de correo electrónico (`EmailStr`).

2. **Definir un modelo de salida:** Crea una clase `RegistroSalida` que herede de `RegistroEntrada` y agregue un campo `id` entero. Incluye `class Config: from_attributes = True` si planeas leer desde objetos SQLAlchemy más adelante.

3. **Endpoint POST de creación:** Crea un endpoint `POST /registros` que reciba un objeto `RegistroEntrada`, le asigne un ID automático (contador en memoria), lo guarde en una lista y devuelva el objeto completo con el ID asignado. Usa `status_code=201` y `response_model=RegistroSalida`.

4. **Endpoint GET de listado:** Crea un endpoint `GET /registros` que devuelva la lista completa de registros creados, validada por `List[RegistroSalida]`.

5. **Endpoint GET por ID:** Crea un endpoint `GET /registros/{id}` que busque un registro por su ID en la lista. Si no existe, lanza una `HTTPException` con código 404 y un mensaje descriptivo.

6. **Endpoint PUT de actualización:** Crea un endpoint `PUT /registros/{id}` que reciba los datos actualizados (`RegistroEntrada`), busque el registro por ID, actualice sus campos y lo devuelva. Si no existe, lanza `HTTPException` 404.

7. **Endpoint DELETE:** Crea un endpoint `DELETE /registros/{id}` que elimine un registro por ID y devuelva un mensaje de confirmación. Si no existe, lanza `HTTPException` 404.

8. **Probar validaciones:** Intenta enviar datos inválidos a través de `/docs` (por ejemplo, un `valor` negativo, un `nombre` de 2 caracteres o un `email` mal formado) y verifica que FastAPI devuelva error 422 con el detalle del problema.

## Resultado esperado

- Dos modelos Pydantic definidos: uno de entrada con validaciones y uno de salida con ID.
- Cinco endpoints funcionales: POST (crear), GET (listar), GET por ID, PUT (actualizar), DELETE.
- Los datos de entrada se validan automáticamente; los envíos inválidos devuelven error 422.
- Los registros no encontrados devuelven error 404 con mensaje claro.
- La documentación en `/docs` muestra los modelos y permite probar cada endpoint con ejemplos de JSON válidos e inválidos.
- Los datos persisten en memoria mientras el servidor esté ejecutándose.

## Pistas

- `Field(..., min_length=3, max_length=100)` hace un campo obligatorio con restricciones de longitud.
- `Field(default=False)` hace un campo opcional con valor por defecto.
- `EmailStr` valida que el texto sea un correo electrónico válido.
- `response_model=RegistroSalida` controla qué campos se devuelven en la respuesta.
- `raise HTTPException(status_code=404, detail="No encontrado")` devuelve un error HTTP personalizado.

## Dificultad

Intermedio

---