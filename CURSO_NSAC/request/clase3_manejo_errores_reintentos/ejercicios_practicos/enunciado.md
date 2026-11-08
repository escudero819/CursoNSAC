# Ejercicios Prácticos - Clase 3: Manejo de errores y reintentos con `requests`

## Objetivo
Blindar las peticiones HTTP contra fallos de red, respuestas inválidas y caídas temporarias de la API, implementando reintentos con espera progresiva y sesiones reutilizables.

## Qué hay que hacer

1. **Petición segura con try/except:** Escribe una función que reciba una URL y realice una petición GET. Envuelve la petición en bloques `try/except` que capturen al menos: `HTTPError`, `ConnectionError`, `Timeout` y una excepción genérica de `requests`. Cada excepción debe imprimir un mensaje diferente y distintivo.

2. **Validar estado con raise_for_status:** Dentro de la función anterior, usa `response.raise_for_status()` para lanzar automáticamente una excepción cuando el código de estado sea 4xx o 5xx. Prueba con una URL que devuelva 404 y verifica que se capture el `HTTPError`.

3. **Reintentos con backoff exponencial:** Implementa un bucle que reintente una petición fallida hasta 3 veces. Entre cada intento, espera un tiempo que crezca progresivamente (por ejemplo, 2 segundos, luego 4, luego 6). Si todos los intentos fallan, devuelve `None` o un mensaje indicando que se agotaron los reintentos.

4. **Sesión reutilizable para múltiples peticiones:** Crea una `requests.Session()` y configura cabeceras por defecto (por ejemplo, `User-Agent` y `Accept`). Usa esa sesión para hacer al menos 3 peticiones GET seguidas al mismo servidor y mide (o comenta) por qué es más eficiente que crear una nueva conexión cada vez.

5. **Plan B ante fallo persistente:** Diseña una lógica donde, si una petición a la API externa falla después de todos los reintentos, el programa recurra a datos locales de respaldo (puede ser un diccionario o JSON hardcodeado) y continúe la ejecución usando esos datos en lugar de detenerse.

6. **Prueba con la API de la NASA:** Aplica el manejo de errores y reintentos a una consulta real de la NASA (por ejemplo, NeoWs). Simula un fallo temporal cambiando intencionalmente la API key o usando una fecha inválida, y observa cómo se recupera tu programa.

## Resultado esperado

- Una función reutilizable `peticion_segura(url)` que nunca falle sin control, capturando todos los tipos de error de `requests`.
- Un mecanismo de reintento que espere progresivamente más tiempo entre intentos.
- Una sesión compartida usada para al menos tres peticiones consecutivas.
- Un plan B funcional: datos locales que se usan cuando la API externa no responde tras varios intentos.
- Prueba ejecutada contra la API de la NASA demostrando recuperación ante un error simulado.

## Pistas

- Importa las excepciones desde `requests.exceptions`.
- `time.sleep(segundos)` permite pausar la ejecución entre reintentos.
- `with requests.Session() as sesion:` asegura que la sesión se cierre correctamente al terminar.

## Dificultad

Intermedio

---