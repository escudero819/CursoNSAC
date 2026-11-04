# Diccionario de sintaxis rápida - `pandas`

## Instalación
```bash
pip install pandas
```

## Importación
```python
import pandas as pd
```

## Crear estructuras

| Operación | Sintaxis |
|-----------|----------|
| Series | `pd.Series([1, 2, 3], index=["a", "b", "c"])` |
| DataFrame desde dict | `pd.DataFrame({"col1": [1, 2], "col2": ["x", "y"]})` |
| DataFrame desde lista de dict | `pd.DataFrame([{"a": 1}, {"a": 2}])` |

## Leer archivos

| Operación | Sintaxis |
|-----------|----------|
| Leer CSV | `df = pd.read_csv("archivo.csv", sep=",", encoding="utf-8")` |
| Leer JSON | `df = pd.read_json("archivo.json")` |
| Leer JSON con líneas | `df = pd.read_json("archivo.jsonl", lines=True)` |
| Leer Excel | `df = pd.read_excel("archivo.xlsx")` |

## Explorar datos

| Método | Para qué sirve |
|--------|----------------|
| `df.head(n)` | Primeras n filas (default 5) |
| `df.tail(n)` | Últimas n filas |
| `df.info()` | Tipos, nulos, uso de memoria |
| `df.describe()` | Estadísticas resumidas |
| `df.shape` | Tupla (filas, columnas) |
| `df.columns` | Nombres de columnas |
| `df.isnull().sum()` | Cantidad de nulos por columna |
| `df.nunique()` | Valores únicos por columna |

## Seleccionar y filtrar

| Operación | Sintaxis |
|-----------|----------|
| Una columna | `df["columna"]` (devuelve Series) |
| Varias columnas | `df[["col1", "col2"]]` (devuelve DataFrame) |
| Filtrar filas | `df[df["col"] > 10]` |
| Filtro combinado | `df[(df["a"] > 1) & (df["b"] < 5)]` |
| Por posición | `df.iloc[0]` (primera fila) |
| Por etiqueta | `df.loc[0]` (fila con índice 0) |
| Resetear índice | `df.reset_index(drop=True)` |

## Transformar JSON anidado

```python
# Aplanar JSON jerárquico a columnas planas
df = pd.json_normalize(lista_de_diccionarios, sep="_")
```

## Agrupar y agregar

| Operación | Sintaxis |
|-----------|----------|
| Contar por grupo | `df.groupby("col").size().reset_index(name="n")` |
| Promedio por grupo | `df.groupby("col")["valor"].mean().reset_index()` |
| Suma por grupo | `df.groupby("col")["valor"].sum().reset_index()` |
| Máximo por grupo | `df.groupby("col")["valor"].max().reset_index()` |

## Combinar DataFrames

| Operación | Sintaxis |
|-----------|----------|
| Unir por columna (JOIN) | `pd.merge(df1, df2, on="id", how="inner")` |
| Apilar filas (UNION) | `pd.concat([df1, df2], ignore_index=True)` |

## Limpiar datos

| Operación | Sintaxis |
|-----------|----------|
| Eliminar nulos | `df.dropna()` |
| Rellenar nulos | `df.fillna(0)` |
| Renombrar columnas | `df.rename(columns={"vieja": "nueva"})` |
| Eliminar duplicados | `df.drop_duplicates()` |
| Copia segura | `df_filtrado = df[condicion].copy()` |

## Exportar

| Operación | Sintaxis |
|-----------|----------|
| Exportar CSV | `df.to_csv("salida.csv", index=False, encoding="utf-8")` |
| Exportar Excel | `df.to_excel("salida.xlsx", index=False)` (necesita openpyxl) |
| Exportar a SQL | `df.to_sql("tabla", con=engine, if_exists="replace", index=False)` |
| Leer de SQL | `df = pd.read_sql_table("tabla", con=engine)` |
| Leer consulta SQL | `df = pd.read_sql("SELECT * FROM tabla", con=engine)` |

---

> **Tip:** Usa `.copy()` al crear subconjuntos para evitar el `SettingWithCopyWarning`.