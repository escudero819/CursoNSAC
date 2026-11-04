# CURSO_NSAC

**Curso inmersivo de manejo de datos, conectividad a APIs REST y base de datos local para la Hackathon NASA Space Apps Challenge (NSAC)**

---

## Rol del instructor

Eres un master en programación, experto en manejo de datos, conectividad a APIs REST y externas, bases de datos locales y disponibilidad de datos según las necesidades del proyecto. También eres profesor experto capaz de dictar cursos inmersivos, fáciles de entender, que permitan a los alumnos adaptar las herramientas enseñadas.

## Objetivo del curso

Que un licenciado en Ciencias de Datos (o cualquier participante de la hackathon) sea capaz de:

1. Consultar APIs externas (especialmente la de la NASA) usando `requests`.
2. Procesar, transformar y analizar los datos recibidos con `pandas`.
3. Almacenar los datos en una base de datos local con `SQLite` / `SQLAlchemy`.
4. Exponer esos datos mediante APIs REST locales con `FastAPI`.
5. Entender el razonamiento lógico de un data scientist ante problemas reales de la competencia.
6. Anticipar errores comunes y saber adaptarse rápidamente bajo presión.

## Estructura de carpetas

```
CURSO_NSAC/
├── README.md                                          <- Esta guía general
├── request/                                           <- Librería requests (peticiones HTTP)
│   ├── clase1_peticiones_basicas/
│   ├── clase2_conexion_api_nasa/
│   └── clase3_manejo_errores_reintentos/
├── pandas/                                            <- Librería pandas (manejo de datos)
│   ├── clase1_estructuras_datos/
│   ├── clase2_transformacion_json_api/
│   └── clase3_exportar_a_sql/
├── sqlite_sqlalchemy/                                 <- Base de datos local
│   ├── clase1_sqlite_basico/
│   ├── clase2_orm_sqlalchemy/
│   └── clase3_integracion_api_bd/
├── fastapi/                                           <- APIs REST locales
│   ├── clase1_endpoints_basicos/
│   ├── clase2_modelos_pydantic/
│   ├── clase3_crud_con_bd/
│   └── clase4_integracion_nasa_endpoints/
├── Diccionario_sintaxis/                              <- Consultas rápidas de sintaxis
│   ├── requests.md
│   ├── pandas.md
│   ├── sqlalchemy.md
│   └── fastapi.md
└── Consejos_buenas_practicas.md                       <- Consejos y buenas prácticas para la hackathon
```

Cada carpeta de clase contiene:

| Archivo / Carpeta | Contenido |
|-------------------|-----------|
| `app.py` | Programa práctico ejecutable con la clase |
| `explicacion_clase.md` | Explicación detallada: qué hace el ejemplo, cómo funciona la clase, diccionario de sintaxis local, flujo de trabajo, errores posibles y soluciones |
| `recursos/` | Archivos de apoyo (JSON de ejemplo, scripts auxiliares, imágenes de flujo) |

## Cómo usar este curso para aprender rápido

1. **Lee primero** el archivo `Diccionario_sintaxis/` para tener a mano los comandos más usados.
2. **Recorre las clases en orden** dentro de cada librería (clase 1 → 2 → 3 → 4).
3. **Ejecuta cada `app.py`** y modifícalo para romperlo y repararlo; eso te enseñará más que solo leerlo.
4. **Lee la `explicacion_clase.md`** de cada clase para entender el razonamiento lógico detrás del código.
5. **Revisa `Consejos_buenas_practicas.md`** antes de empezar la hackathon para evitar errores de principiante.

## Prerrequisitos

Instala las dependencias necesarias:

```bash
pip install requests pandas sqlalchemy fastapi uvicorn
```

## Flujo de trabajo recomendado para la competencia (NSAC)

```
Paso 1: Identificar la fuente de datos (API de la NASA, CSV, JSON, etc.)
Paso 2: Consultar la API con requests y validar la respuesta
Paso 3: Limpiar y transformar los datos con pandas
Paso 4: Almacenar los datos relevantes en SQLite (local) mediante SQLAlchemy
Paso 5: Exponer los datos con FastAPI para que el equipo los consuma
Paso 6: Iterar: manejar errores, reintentar, optimizar consultas
```

## Tecnologías utilizadas

| Herramienta | Propósito en el proyecto |
|-------------|--------------------------|
| `requests` | Peticiones HTTP a APIs externas (NASA y otras) |
| `pandas` | Manipulación, limpieza y análisis de datos (DataFrames, JSON) |
| `SQLite` | Motor de base de datos local ligero, sin servidor |
| `SQLAlchemy` | ORM y capa de abstracción sobre SQLite |
| `FastAPI` | Creación rápida de APIs REST y endpoints locales |

---

> **Nota del profesor:** En una hackathon el tiempo es limitado. Este curso está diseñado para que entiendas el **porqué** de cada línea de código, no solo el **cómo**. Así podrás adaptar las herramientas a cualquier problema que se presente durante la competencia.