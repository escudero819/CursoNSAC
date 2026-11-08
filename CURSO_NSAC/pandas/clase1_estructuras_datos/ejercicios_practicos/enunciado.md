# Ejercicios Prácticos - Clase 1: Estructuras de datos con `pandas`

## Objetivo
Dominar la creación de Series y DataFrames, la carga de datos desde JSON y CSV, y la exploración rápida de conjuntos de datos para entender su estructura en segundos.

## Qué hay que hacer

1. **Crear una Series:** Construye una Series de pandas con los nombres de al menos 5 cuerpos celestes (planetas, lunas o asteroides) y su distancia promedio al Sol en millones de kilómetros. Asigna el nombre de cada cuerpo como índice de la Series. Imprime la Series y consulta el valor de uno de los cuerpos por su nombre (índice).

2. **Crear un DataFrame desde diccionario:** Construye un DataFrame con al menos 4 columnas y 6 filas de datos espaciales (por ejemplo: nombre, tipo, diámetro, masa, distancia al Sol, fecha de descubrimiento). Los datos pueden ser inventados o basados en información real de la NASA. Muestra el DataFrame completo.

3. **Cargar datos desde un archivo JSON:** Crea un archivo JSON con una lista de al menos 5 objetos que representen eventos espaciales (fecha, tipo de evento, ubicación, magnitud). Cárgalo con `pd.read_json()` e imprime las primeras filas con `head()`.

4. **Cargar datos desde un archivo CSV:** Crea un archivo CSV con al menos 8 filas de datos sobre asteroides (nombre, diámetro, velocidad, fecha de acercamiento, potencialmente peligroso). Cárgalo con `pd.read_csv()` y verifica que se lea correctamente.

5. **Explorar un DataFrame:** Sobre cualquiera de los DataFrames creados, ejecuta y muestra en consola el resultado de: `head()`, `info()`, `describe()`, `shape`, `columns` y `isnull().sum()`. Interpreta brevemente qué te dice cada uno sobre tus datos.

6. **Seleccionar y filtrar datos:** Sobre el DataFrame de asteroides, haz lo siguiente:
   - Selecciona solo la columna "nombre" y muéstrala.
   - Selecciona dos columnas a la vez (por ejemplo, nombre y diámetro).
   - Filtra solo los asteroides potencialmente peligrosos.
   - Filtra los asteroides con diámetro mayor a un valor que tú elijas.
   - Accede a la primera fila usando `iloc` y a una fila por su etiqueta de índice usando `loc`.

## Resultado esperado

- Una Series correctamente indexada y consultable por nombre.
- Un DataFrame con al menos 4 columnas y 6 filas, impreso en consola.
- Un archivo JSON cargado y mostrado con `head()`.
- Un archivo CSV cargado y mostrado con `head()`.
- Salida en consola de los seis métodos de exploración (`head`, `info`, `describe`, `shape`, `columns`, `isnull().sum()`).
- Al menos cinco operaciones de selección y filtrado ejecutadas sobre el DataFrame, cada una con su resultado impreso.
- Ningún error de clave o índice al ejecutar las operaciones.

## Pistas

- Para crear una Series con índice personalizado, usa el parámetro `index=`.
- `pd.read_json()` funciona bien si el JSON es una lista de diccionarios.
- Usa `df["columna"]` para una columna y `df[["col1", "col2"]]` para varias.
- Para filtrar, usa una condición booleana dentro de corchetes: `df[df["columna"] > valor]`.
- `iloc` accede por posición numérica; `loc` accede por etiqueta de índice.

## Dificultad

Principiante

---