# Integración de librerías en un sistema real

Esta carpeta contiene una clase dedicada a mostrar cómo integrar **todas las librerías del curso** (`requests`, `pandas`, `SQLAlchemy/SQLite`, `FastAPI`) en un único sistema coherente, listo para usar en la hackathon NSAC.

## Estructura

```
integracion_sistema/
└── clase1_sistema_integrado_nasa/
    ├── app.py                    <- Sistema completo integrado
    ├── explicacion_clase.md      <- Explicación detallada
    ├── ejercicios_practicos/
    │   └── enunciado.md          <- Qué hacer sin código específico
    └── recursos/                 <- Archivos de apoyo
```

## Qué aprenderás aquí

- Cómo unir las cuatro librerías en un flujo ETL + API real.
- Cómo evitar llamar repetidamente a la API de la NASA (caché local en SQLite).
- Cómo exponer los datos almacenados mediante endpoints FastAPI para todo el equipo.
- Cómo manejar errores de red, de base de datos y de validación en un mismo sistema.
- Estructura recomendada de archivos para un proyecto de hackathon.

## Prerrequisitos

Habrás completado todas las clases previas de `request`, `pandas`, `sqlite_sqlalchemy` y `fastapi`.

```
pip install requests pandas sqlalchemy fastapi uvicorn
```