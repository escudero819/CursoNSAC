# Clase 1 - Estructuras de datos con `pandas`

## 1. Explicación del ejemplo

En esta clase aprendes las dos estructuras fundamentales de **pandas**, la librería más usada para manejo y análisis de datos en Python:

- **Series:** Un arreglo unidimensional etiquetado (como una columna de Excel).
- **DataFrame:** Una tabla bidimensional con filas y columnas (como una hoja de Excel o una tabla de SQL).

El archivo `app.py` contiene cuatro ejemplos:

1. **Crear Series y DataFrame:** Desde diccionarios y listas de Python.
2. **Leer JSON y CSV:** Cargar datos desde archivos (útil para datos de la NASA exportados).
3. **Explorar datos:** `head()`, `info()`, `describe()` para entender los datos en segundos.
4. **Seleccionar y filtrar:** Obtener columnas específicas y filtrar filas con condiciones.

---

## 2. Explicación de la clase / conceptos clave

### Series vs DataFrame

| Característica | Series | DataFrame |
|----------------|--------|-----------|
| Dimensiones | 1D (una columna) | 2D (filas y columnas) |
| Índice | Etiquetas de fila | Etiquetas de fila + nombre de columnas |
| Uso típico | Una sola variable | Tabla completa de datos |

### Crear un DataFrame

```python
import pandas as pd

# Desde diccionario de listas
datos = {"nombre": ["Marte", "Júpiter"], "tipo": ["planeta", "planeta"]}
df = pd.DataFrame(datos)

# Desde lista de diccionarios (muy común con JSON de APIs)
datos = [
    {"nombre": "Marte", "tipo": "planeta"},
    {"nombre": "Fobos", "tipo": "luna"}
]
df = pd.DataFrame(datos)
```

### Leer datos desde archivos

```python
df_json = pd.read_json("archivo.json")
df_csv = pd.read_csv("archivo.csv", sep=",", encoding="utf-8")
```

### Exploración rápida

| Método | Para qué sirve |
|--------|----------------|
| `df.head(n)` | Primeras `n` filas (default 5) |
| `df.info()` | Tipos de datos, valores nulos, memoria |
| `df.describe()` | Estadísticas resumidas (media, std, min, max) |
| `df.shape` | Tupla (filas, columnas) |
| `df.columns` | Nombres de las columnas |
| `df.isnull().sum()` | Cantidad de valores nulos por columna |

### Selección y filtrado

```python
# Una columna (devuelve Series)
columna = df["nombre"]

# Varias columnas (devuelve DataFrame)
subset = df[["nombre", "diametro_km"]]

# Filtrar filas con condición
peligrosos = df[df["peligroso"] == True]
grandes = df[df["diametro_km"] > 0.1]

# Por posición (índice numero)
fila = df.iloc[0]          # primera fila
fila_etiqueta = df.loc[2]  # fila con índice 2
```

---

## 3. Diccionario de sintaxis global - `pandas` (clase 1)

```python
import pandas as pd

# Crear DataFrame
df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})

# Leer archivos
df = pd.read_csv("archivo.csv")
df = pd.read_json("archivo.json")

# Explorar
df.head()
df.info()
df.describe()
df.shape
df.columns

# Seleccionar
df["columna"]
df[["col1", "col2"]]
df[df["col1"] > 10]          # filtrar filas
df.iloc[0]                   # por posición
df.loc[0]                    # por etiqueta de índice

# Valores nulos
df.isnull().sum()
df.dropna()                  # eliminar filas con nulos
df.fillna(0)                 # rellenar nulos con 0
```

---

## 4. Flujo de trabajo lógico

1. **Cargar los datos:** Desde JSON de la API, CSV, o crear desde diccionarios.
2. **Explorar:** Usar `head()`, `info()`, `describe()` para entender qué tienes.
3. **Limpiar:** Revisar valores nulos, duplicados, tipos de datos incorrectos.
4. **Seleccionar:** Quedarte solo con las columnas que necesitas.
5. **Filtrar:** Quedarte con las filas que cumplen condiciones (ej. solo asteroides peligrosos).

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `FileNotFoundError` | El archivo no existe | Verificar la ruta del archivo |
| `KeyError` | La columna no existe | Revisar `df.columns` para escribir el nombre bien |
| `ValueError` | JSON mal formado | Verificar que el archivo JSON sea válido |
| `SettingWithCopyWarning` | Modificando un fragmento del DataFrame | Usar `.copy()` al crear subconjuntos: `df_filtrado = df[condicion].copy()` |

---

## 6. Adaptación a la competencia NSAC

En la hackathon recibirás JSON de la API de la NASA. El flujo típico será:

1. `requests.get()` → obtienes JSON
2. `pd.DataFrame(json)` o `pd.read_json()` → lo conviertes en DataFrame
3. `df.head()` y `df.info()` → entiendes la estructura
4. Filtras y seleccionas los datos relevantes
5. Lo guardas en SQLite o lo expones con FastAPI

Siguiente paso sugerido: `clase2_transformacion_json_api` para aprender a aplanar JSON anidados (muy común en respuestas de la NASA).