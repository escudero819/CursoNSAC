# Clase 2 - Transformación de JSON de APIs con `pandas`

## 1. Explicación del ejemplo

Las APIs REST (incluida la de la NASA) devuelven frecuentemente JSON **anidados**: diccionarios dentro de diccionarios, listas dentro de diccionarios, etc. pandas no puede leer eso directamente como una tabla plana, por eso necesitamos aplanar los datos.

Este archivo contiene cuatro ejemplos:

1. **Aplanar JSON anidado:** Usar `pd.json_normalize()` para convertir JSON jerárquico (tipo NeoWs de la NASA) en un DataFrame con columnas planas.
2. **Filtrar, agrupar y agregar:** Seleccionar datos según condiciones, contar por grupo, calcular promedios.
3. **Combinar DataFrames:** `merge` (como JOIN en SQL) y `concat` (apilar tablas).
4. **Exportar:** Guardar el resultado en CSV y Excel.

---

## 2. Explicación de la clase / conceptos clave

### `pd.json_normalize()`

Esta función es clave cuando trabajas con APIs. Recibe una lista de diccionarios y aclara las claves anidadas usando un separador (por defecto `_`):

```python
# Antes (anidado):
{"nombre": "Asteroide", "diametro": {"km": {"min": 0.1, "max": 0.2}}}

# Después (plano con sep="_"):
nombre | diametro_km_min | diametro_km_max
Asteroide | 0.1 | 0.2
```

### Filtrado booleano

```python
df[df["columna"] == valor]          # filas donde columna es igual a valor
df[df["columna"] > 10]              # filas donde columna es mayor a 10
df[(df["a"] > 1) & (df["b"] < 5)]   # condiciones combinadas con & (y) | (o)
```

### Agrupación y agregación

```python
df.groupby("columna").size()                     # contar por grupo
df.groupby("columna")["otra_columna"].mean()     # promedio por grupo
df.groupby("columna")["otra_columna"].sum()      # suma por grupo
```

### Combinar DataFrames

| Operación | Uso | Equivalente SQL |
|-----------|-----|-----------------|
| `pd.merge(df1, df2, on="id")` | Unir por columna común | `INNER JOIN` |
| `pd.concat([df1, df2])` | Apilar filas verticalmente | `UNION ALL` |

### Exportación

```python
df.to_csv("archivo.csv", index=False, encoding="utf-8")
df.to_excel("archivo.xlsx", index=False)  # requiere openpyxl
```

---

## 3. Diccionario de sintaxis global - `pandas` (clase 2)

```python
import pandas as pd

# Aplanar JSON anidado
df = pd.json_normalize(lista_de_diccionarios, sep="_")

# Filtrar
df_filtrado = df[df["columna"] == valor]
df_filtrado = df[(df["a"] > 1) & (df["b"] < 5)]

# Agrupar
conteo = df.groupby("columna").size().reset_index(name="n")
promedio = df.groupby("columna")["valor"].mean().reset_index()

# Combinar
df_unido = pd.merge(df1, df2, on="id_comun", how="inner")
df_apilado = pd.concat([df1, df2], ignore_index=True)

# Exportar
df.to_csv("salida.csv", index=False)
df.to_excel("salida.xlsx", index=False)
```

---

## 4. Flujo de trabajo lógico

1. **Obtener el JSON:** De la API con `requests`.
2. **Extraer la lista relevante:** Si el JSON tiene claves anidadas como `near_earth_objects`, navegar hasta la lista.
3. **Aplanar:** `pd.json_normalize()` para obtener columnas planas.
4. **Limpiar y filtrar:** Quedarte con las columnas y filas que necesitas.
5. **Agrupar/agregar:** Calcular conteos, promedios, máximos según lo que pida el problema.
6. **Combinar:** Si tienes datos de varias fuentes, unir con `merge`.
7. **Exportar:** Guardar en CSV/Excel o pasar a SQLite.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `KeyError` | Clave anidada no existe | Verificar la estructura del JSON antes de normalizar |
| `ValueError` | `json_normalize` recibe un diccionario, no una lista | Pasar una lista de diccionarios, no un solo diccionario |
| Columnas con nombres muy largos | Anidación profunda crea nombres largos | Renombrar columnas con `df.rename(columns={...})` |
| `ModuleNotFoundError: openpyxl` | Intentar exportar a Excel sin la librería | Usar CSV o instalar: `pip install openpyxl` |

---

## 6. Adaptación a la competencia NSAC

La respuesta de NeoWs de la NASA tiene exactamente esta estructura anidada. Con `pd.json_normalize()` puedes convertirla en una tabla limpia y luego:

- Filtrar solo asteroides peligrosos.
- Contar cuántos hay por día.
- Calcular el diámetro máximo promedio.
- Unir con otros DataFrames (por ejemplo, datos meteorológicos de otra API).

Siguiente paso sugerido: `clase3_exportar_a_sql` para aprender a guardar estos DataFrames en una base de datos SQLite local.