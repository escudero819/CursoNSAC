# Ejercicios Prácticos - Clase 4: Integración con API de la NASA en FastAPI

## Objetivo
Crear endpoints de FastAPI que consuman datos de la API de la NASA, los guarden en SQLite local como caché, eviten llamadas repetidas innecesarias y expongan los datos almacenados al equipo mediante endpoints REST.

## Qué hay que hacer

1. **Definir el modelo de eventos:** Crea un modelo SQLAlchemy para almacenar eventos de la NASA con al menos estos campos: id, fuente (texto, ej. "EONET"), título, descripción, fecha del evento, URL de origen y fecha de guardado.

2. **Función de consulta a la NASA:** Escribe una función auxiliar que consulte un endpoint de la NASA (por ejemplo, EONET para eventos naturales) con `requests`, maneje errores de red con `try/except` y devuelva la lista de eventos o una lista vacía si falla.

3. **Función de guardado con evitación de duplicados:** Escribe una función que reciba la lista de eventos y una sesión de base de datos. Para cada evento, verifique si ya existe en SQLite (por título + fecha) antes de insertar. Cuente cuántos se insertaron y cuántos se omitieron.

4. **Endpoint de sincronización:** Crea un endpoint `POST /sincronizar-nasa` que llame a la función de consulta, guarde los eventos en la base de datos y devuelva un mensaje con la cantidad de eventos sincronizados. Usa `BackgroundTasks` para que la sincronización no bloquee la respuesta HTTP.

5. **Endpoint de listado local:** Crea un endpoint `GET /eventos` que devuelva los eventos guardados en SQLite. Agrega filtros opcionales por fuente y un límite de resultados.

6. **Endpoint de obtener uno y eliminar:** Crea endpoints `GET /eventos/{id}` y `DELETE /eventos/{id}` para consultar y eliminar eventos individuales guardados localmente.

7. **Manejo de fallos de la NASA:** Si la API de la NASA no responde o devuelve error, el endpoint de sincronización debe devolver un error HTTP 503 con un mensaje claro, sin que el servidor se caiga.

8. **Probar el flujo completo:** Levanta el servidor, sincroniza eventos desde la NASA, consulta los eventos guardados localmente, y verifica que al sincronizar nuevamente con las mismas fechas no se dupliquen registros.

## Resultado esperado

- Un archivo `.db` de SQLite con la tabla de eventos de la NASA.
- Cinco endpoints funcionales: sincronización, listado, obtener uno, eliminar y raíz.
- La sincronización use `BackgroundTasks` para no bloquear la respuesta.
- Los datos de la NASA se guarden en SQLite y se puedan consultar sin llamar nuevamente a la API externa.
- Se eviten duplicados al sincronizar dos veces con el mismo rango de fechas.
- Si la API de la NASA falla, el servidor devuelva error 503 controlado en lugar de caer.
- La documentación `/docs` muestre todos los endpoints y permita probar la sincronización y consulta.

## Pistas

- `BackgroundTasks` permite ejecutar una función después de enviar la respuesta HTTP: `background_tasks.add_task(funcion, argumento)`.
- Para evitar duplicados: `db.query(Modelo).filter(Modelo.titulo == titulo, Modelo.fecha_evento == fecha).first()`.
- Usa `try/except requests.exceptions.RequestException` alrededor de la llamada a la NASA.
- `response_model=List[ModeloRespuesta]` en el endpoint de listado para validar la salida.

## Dificultad

Avanzado

---