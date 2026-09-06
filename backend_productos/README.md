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
- urllib.request
- urllib.error

## Puerto

MS-Categoria:
```text
http://localhost:8085
```

MS-Producto:
```text
http://localhost:8086
```

## Arquitectura

```text
ProductoController
        |
        v
     ProductoN
      /     \
     v       v
ProductoDao  CategoriaClient
     |             |
     v             v
 PostgreSQL    MS-Categoria
              localhost:8085
```

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

## Comunicación entre microservicios

Antes de crear o actualizar un producto,
`ProductoN` utiliza `CategoriaClient.existeCategoria(codigo)`
para consultar:

```text
GET http://localhost:8085/categorias/{codigo}
```

Por lo tanto, para probar Producto con validación de categoría,
primero debe estar ejecutándose MS-Categoria en el puerto 8085.

## Base de datos

Editar `conexion.py` con los datos reales de PostgreSQL.

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

para correr se usa python producto_servidor.py