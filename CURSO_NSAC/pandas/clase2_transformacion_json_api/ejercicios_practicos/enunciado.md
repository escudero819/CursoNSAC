# Ejercicios Prácticos - Clase 2: Transformación de JSON de APIs con `pandas`

## Objetivo
Aprender a aplanar JSON anidados (típicos de las respuestas de la NASA) en tablas planas, filtrar y agrupar datos, combinar múltiples DataFrames y exportar los resultados a archivos externos.

## Qué hay que hacer

1. **Aplanar un JSON anidado:** Consigue un JSON con estructura anidada (puedes usar la respuesta de ejemplo de NeoWs de la NASA o crear uno tú). Usa `pd.json_normalize()` para convertirlo en un DataFrame plano donde cada clave anidada se convierta en una columna separada (usando un separador como `_`). Imprime los nombres de las columnas resultantes.

2. **Extraer la lista correcta antes de normalizar:** Si el JSON tiene una estructura como `{"near_earth_objects": {"fecha": [lista de asteroides]}}`, primero navega hasta la lista de asteroides y luego aplánala. Agrega la fecha como una columna adicional en cada fila.

3. **Filtrar datos transformados:** Sobre el DataFrame aplanado, filtra para quedarte solo con los asteroides potencialmente peligrosos. También filtra los que tengan un diámetro máximo mayor a un umbral que tú definas (por ejemplo, 0.5 km).

4. **Agrupar y agregar datos:** Agrupa los asteroides por fecha de acercamiento y cuenta cuántos hay por día. También calcula el diámetro máximo promedio por fecha. Muestra ambos resultados en consola.

5. **Combinar DataFrames:** Crea dos DataFrames pequeños relacionados (por ejemplo, uno con información de asteroides y otro con sus acercamientos). Únelos con `pd.merge()` usando una columna común (como un ID). Luego crea un tercer DataFrame y apílalo verticalmente con `pd.concat()`.

6. **Exportar a CSV y Excel:** Exporta el DataFrame final (después de filtrar, agrupar o combinar) a un archivo CSV sin incluir el índice. Intenta exportarlo también a Excel (necesitarás instalar `openpyxl` si no lo tienes). Verifica que los archivos se crearon en tu carpeta.

## Resultado esperado

- Un DataFrame plano obtenido de un JSON anidado, con columnas claras y sin diccionarios dentro de celdas.
- Al menos dos filtros aplicados al DataFrame (peligrosos y por diámetro), cada uno con su resultado impreso.
- Una agrupación por fecha con conteo y un promedio calculado, mostrados en consola.
- Un DataFrame combinado mediante `merge` (al menos dos tablas unidas).
- Un DataFrame apilado mediante `concat` (al menos dos tablas verticalmente).
- Un archivo CSV exportado correctamente en tu carpeta de trabajo.
- (Opcional) Un archivo Excel exportado, si se pudo instalar `openpyxl`.

## Pistas

- `pd.json_normalize(lista, sep="_")` aclara claves anidadas como `diametro_kilometers_maximo`.
- Para navegar un JSON anidado, usa bucles `for` sobre las claves intermedias antes de crear la lista final.
- `df.groupby("columna").size()` cuenta elementos por grupo.
- `pd.merge(df1, df2, on="id_comun")` une tablas como un JOIN en SQL.
- `df.to_csv("archivo.csv", index=False)` evita escribir el índice de pandas como columna extra.

## Dificultad

Intermedio

---