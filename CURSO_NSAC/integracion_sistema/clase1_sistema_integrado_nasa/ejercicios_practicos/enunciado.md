# Ejercicios Prácticos - Clase 1: Sistema integrado (NASA + pandas + SQLite + FastAPI)

## Objetivo
Construir un sistema completo que integre las cuatro librerías del curso en un flujo real: extraer datos de la NASA, transformarlos con pandas, guardarlos en SQLite y exponerlos mediante FastAPI, sin depender de llamadas repetidas a la API externa.

## Qué hay que hacer

1. **Diseñar el modelo de datos:** Decidir qué información guardar de la NASA (por ejemplo: fuente, nombre, fecha, descripción, diámetro, si es peligroso, distancia, velocidad, URL de origen). Definir las columnas y tipos de datos de la tabla en SQLite.

2. **Configurar la base de datos:** Crear el engine de SQLAlchemy para SQLite, la fábrica de sesiones y la clase base declarativa. Definir el modelo de tabla que coincida con el diseño del paso 1. Crear las tablas al iniciar el programa.

3. **Definir modelos Pydantic:** Crear al menos tres modelos: uno para los datos de entrada (lo que se recibe de la NASA o se envía al crear), uno para crear registros y uno para la respuesta (que incluya el ID y tenga `from_attributes = True`).

4. **Crear la dependency de sesión:** Escribir una función `get_db()` que cree una sesión, la entregue con `yield` y la cierre en un bloque `finally`. Usarla como dependencia en todos los endpoints que accedan a la base de datos.

5. **Implementar la extracción de datos:** Escribir funciones que consuman al menos dos endpoints diferentes de la NASA (por ejemplo, NeoWs para asteroides y EONET para eventos naturales). Cada función debe manejar errores de red con `try/except` y retornar una lista de diccionarios normalizados o una lista vacía si falla.

6. **Implementar la transformación con pandas:** Recibir la lista de diccionarios de la NASA y convertirla en un DataFrame plano. Seleccionar solo las columnas relevantes, manejar valores nulos y preparar los datos para guardarlos.

7. **Implementar la carga con evitación de duplicados:** Escribir una función que reciba la lista de eventos transformados y una sesión de base de datos. Para cada evento, verificar si ya existe en SQLite (por fuente + nombre + fecha) antes de insertar. Contar cuántos se insertaron y cuántos se omitieron por ser duplicados.

8. **Crear el endpoint de sincronización:** Un endpoint `POST /sincronizar-nasa` que llame a las funciones de extracción, transforme y cargue en la base de datos. Usar `BackgroundTasks` para que no bloquee la respuesta HTTP. Devolver un mensaje con la cantidad de eventos sincronizados y omitidos.

9. **Crear endpoints de consulta local:** Al menos estos endpoints:
   - `GET /eventos`: listar eventos guardados, con filtros opcionales por fuente y por si son peligrosos.
   - `GET /eventos/{id}`: obtener un evento por su ID local.
   - `DELETE /eventos/{id}`: eliminar un evento guardado.

10. **Crear un endpoint de estadísticas:** Un endpoint que lea los datos de SQLite, los convierta en un DataFrame de pandas y devuelva estadísticas (total de eventos, cuántos son peligrosos, conteo por fuente).

11. **Crear un endpoint de exportación:** Un endpoint que exporte los datos de SQLite a un archivo CSV usando pandas.

12. **Probar el sistema integrado:** Levantar el servidor con uvicorn, sincronizar datos desde la NASA, consultar los eventos guardados localmente, verificar que al sincronizar dos veces no se dupliquen registros, y probar la exportación a CSV.

13. **Manejo de errores integrado:** Asegurar que si la NASA no responde, el servidor devuelva un error HTTP 503 claro en lugar de caerse. Verificar que los registros no encontrados devuelvan error 404.

## Resultado esperado

- Un archivo `app.py` que ejecute un sistema FastAPI completo con al menos 7 endpoints funcionales.
- Un archivo `.db` de SQLite creado con la tabla de eventos espaciales.
- Los datos de la NASA se guarden en SQLite y se puedan consultar sin llamar nuevamente a la API externa.
- La sincronización evite duplicados al ejecutarse dos veces con el mismo rango de fechas.
- Un endpoint de estadísticas que use pandas sobre datos leídos de SQLite.
- Un endpoint de exportación que genere un archivo CSV real en la carpeta.
- Si la API de la NASA falla, el servidor responda con error 503 controlado.
- La documentación automática en `/docs` muestre todos los endpoints y permita probarlos.
- Los datos persistan en el archivo `.db` entre reinicios del servidor.

## Pistas

- Usa `BackgroundTasks` para la sincronización: `background_tasks.add_task(funcion, argumento)`.
- Para evitar duplicados: consulta la base de datos antes de cada `session.add()`.
- `pd.DataFrame(lista_de_diccionarios)` convierte la lista transformada en DataFrame.
- `df.to_csv("archivo.csv", index=False)` exporta sin el índice de pandas.
- `connect_args={"check_same_thread": False}` es necesario para SQLite con FastAPI.
- `response_model=List[ModeloRespuesta]` valida y documenta la salida de listado.

## Dificultad

Avanzado

---