# Resumen de endpoints - Clase 4

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/eventos` | Lista eventos guardados (filtro opcional por `fuente` y `limite`) |
| POST | `/sincronizar-nasa` | Consulta la API de la NASA (EONET) y guarda en SQLite local |
| GET | `/eventos/{id}` | Obtiene un evento por ID |
| DELETE | `/eventos/{id}` | Elimina un evento guardado localmente |

Probar en: `http://127.0.0.1:8000/docs`