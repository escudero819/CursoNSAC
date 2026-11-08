# Ejercicios Prácticos - Clase 2: Conexión a la API de la NASA con `requests`

## Objetivo
Aplicar los conocimientos de `requests` específicamente a los endpoints de la NASA, gestionar la autenticación con API key y navegar por respuestas JSON anidadas para extraer información útil.

## Qué hay que hacer

1. **Consultar la APOD de hoy:** Usa el endpoint `/planetary/apod` de la NASA con tu `API_KEY` (o `DEMO_KEY` para pruebas). Extrae e imprime: título, fecha, explicación (primeros 200 caracteres) y URL de la imagen.

2. **Consultar la APOD de una fecha histórica:** Elige una fecha importante (por ejemplo, una llegada a la Luna o un eclipse) y consulta la APOD de ese día usando el parámetro `date`. Verifica que la fecha en la respuesta coincida con la solicitada.

3. **Consultar asteroides cercanos (NeoWs):** Usa el endpoint `/neo/rest/v1/feed` para consultar asteroides en un rango de fechas (por ejemplo, los últimos 7 días). Cuenta cuántos asteroides se encontraron en total e imprime los nombres de los primeros 5.

4. **Extraer datos anidados de forma segura:** De la respuesta de NeoWs, accede al diámetro estimado en kilómetros de al menos un asteroide. Usa acceso seguro con `.get()` para evitar errores si alguna clave intermedia falta en el JSON.

5. **Identificar asteroides potencialmente peligrosos:** Recorre la lista de asteroides obtenida y filtra solo aquellos donde `is_potentially_hazardous_asteroid` sea `True`. Imprime su nombre, fecha de acercamiento y diámetro máximo.

6. **Manejo de errores de la NASA:** Prueba qué ocurre si usas una API key inválida o si excedes el límite de peticiones. Captura el error y muestra un mensaje que distinga entre error de autenticación (403) y límite excedido (429).

## Resultado esperado

- Un script que consulte al menos tres endpoints distintos de la NASA.
- Por cada consulta, se imprima información legible y estructurada (títulos, fechas, conteos, URLs).
- Se muestre al menos un ejemplo de acceso a datos anidados (diametro dentro de estimated_diameter dentro de kilometers).
- Se identifiquen y separen los asteroides potencialmente peligrosos del resto.
- El programa maneje graciosamente al menos un escenario de error (API key inválida o límite excedido) sin cerrarse.

## Pistas

- La respuesta de NeoWs tiene la estructura: `near_earth_objects` → `fecha` → lista de asteroides → datos anidados.
- Usa `datetime` para generar rangos de fechas en formato `YYYY-MM-DD`.
- Para acceder a claves anidadas sin que el programa falle, encadena `.get("clave", {})` en lugar de usar corchetes directamente.

## Dificultad

Intermedio

---