# Microservicio Producto

Microservicio desarrollado con Python puro, sin Flask, FastAPI,
Django ni otro framework web.

## Dependencia

La unica dependencia externa es:

```bash
pip install psycopg2-binary
```

El resto utiliza librerias de Python:

- http.server
- json
- re

## Puerto

```text
http://localhost:8086
```

Configurable con la variable de entorno `PRODUCTO_SERVICE_PORT`.

## Arquitectura

```text
ProductoController
        |
        v
     ProductoN
        |
        v
   ProductoDao
        |
        v
   PostgreSQL
```

Este microservicio **no llama a ningun otro microservicio**. Solo debe
ser invocado por `services/api-gateway`, nunca directamente desde el
frontend ni desde otro microservicio (por eso no expone CORS).

La validacion de que `categoria_codigo` corresponda a una categoria
existente ya no ocurre aqui: la hace API-Gateway (`producto_orquestador.py`)
antes de reenviar la peticion de creacion/actualizacion a este servicio.

## Endpoints

### Listar

```http
GET http://localhost:8086/productos
```

### Obtener

```http
GET http://localhost:8086/productos/1
```

### Crear

```http
POST http://localhost:8086/productos
Content-Type: application/json

{
  "nombre": "Café molido 500g",
  "precio": 42.50,
  "categoria_codigo": 1
}
```

### Actualizar

```http
PUT http://localhost:8086/productos/1
Content-Type: application/json

{
  "nombre": "Café molido 500g",
  "precio": 45.00,
  "categoria_codigo": 1
}
```

### Eliminar

```http
DELETE http://localhost:8086/productos/1
```

## Base de datos

Editar las variables de entorno `PRODUCTO_DB_HOST`, `PRODUCTO_DB_PORT`,
`PRODUCTO_DB_NAME`, `PRODUCTO_DB_USER`, `PRODUCTO_DB_PASSWORD` con los
datos reales de PostgreSQL (ver `conexion.py` y el `.env.example` en la
raíz del repo).

La implementación espera una tabla con una estructura equivalente a:

```sql
CREATE TABLE producto (
  codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
  categoria_codigo INTEGER NOT NULL
);
```

Si tu tabla utiliza otro nombre de columna para la relación con
categoria, modifica únicamente las consultas de `producto_dao.py`.

Para correr: `python src/producto_servidor.py` (desde
`services/producto-service`).
