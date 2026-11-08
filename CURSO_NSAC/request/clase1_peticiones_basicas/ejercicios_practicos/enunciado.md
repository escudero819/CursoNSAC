# Ejercicios Prácticos - Clase 1: Peticiones HTTP básicas con `requests`

## Objetivo
Consolidar el uso de la librería `requests` para realizar peticiones GET y POST, manejar parámetros de consulta y cabeceras, e interpretar respuestas HTTP sin romper el programa ante fallos.

## Qué hay que hacer

1. **Petición GET pública:** Elige una API pública gratuita (puede ser una de pruebas o la de la NASA con `DEMO_KEY`). Realiza una petición GET a un endpoint que devuelva un único recurso. Imprime en consola el código de estado, el tipo de contenido de la respuesta y al menos dos campos del JSON devuelto.

2. **Petición GET con filtros:** Consulta el mismo endpoint pero agrega al menos dos parámetros de consulta (por ejemplo, limitar cantidad de resultados o filtrar por categoría/fecha). Muestra la URL final que se generó y verifica que la respuesta contenga solo los elementos solicitados.

3. **Petición POST simulada:** Envía datos a un endpoint de prueba que acepte POST (por ejemplo, `https://jsonplaceholder.typicode.com/posts`). Construye un diccionario con al menos tres campos relevantes para tu proyecto (título, cuerpo, ID de usuario, etc.) y envíalo como JSON. Imprime la respuesta del servidor para confirmar que se creó el recurso.

4. **Petición con cabecera personalizada:** Realiza una petición GET incluyendo una cabecera `User-Agent` personalizada que identifique a tu equipo en la hackathon (por ejemplo, `EquipoNSAC/1.0`). Verifica que la cabecera se envía correctamente inspeccionando los headers de la respuesta o usando un servicio que devuelva los headers recibidos.

5. **Manejo básico de fallos:** Intenta hacer una petición a una URL que no exista o que tarde demasiado. Envuelve la petición en un bloque `try/except` para que el programa no se detenga y muestre un mensaje amigable indicando qué tipo de error ocurrió (timeout, conexión, o error HTTP).

## Resultado esperado

- Un script de Python que ejecute las cinco acciones anteriores de forma secuencial.
- Por cada acción, se imprima en consola información clara: éxito o fallo, código de estado HTTP, y datos relevantes extraídos de la respuesta.
- Ante una URL inválida o un servidor caído, el programa debe continuar ejecutando sin cerrarse abruptamente, mostrando el mensaje de error capturado.
- Se debe poder identificar visualmente la diferencia entre una petición con y sin parámetros de consulta (comparando las URLs mostradas).

## Pistas

- Usa siempre `timeout` en tus peticiones para evitar que el programa se quede esperando indefinidamente.
- Para verificar si una petición tuvo éxito, revisa `response.status_code == 200` o usa `response.ok`.
- Para convertir la respuesta a un diccionario de Python, usa `response.json()`.
- Para enviar JSON en una POST, usa el parámetro `json=` de `requests.post()`.

## Dificultad

Principiante

---