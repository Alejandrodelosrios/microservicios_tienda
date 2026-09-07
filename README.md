# Microservicios Tienda

Tienda basada en microservicios, desarrollada con Python puro
(`http.server`, sin Flask/FastAPI/Django) y un frontend estático en
HTML/CSS/JS sin frameworks ni build step.

## Arquitectura

```text
                Frontend (frontend/)
                        |
                        v
                 API Gateway :8080  (services/api-gateway)
          /          |          |          \
         v           v          v           v
  Categoria      Producto    Cliente      Venta
   :8085          :8086       :8087       :8088
(cada uno con su propia base de datos, sin Docker)
```

Regla estricta: **el frontend solo llama al API Gateway, y los
microservicios nunca se llaman entre sí.** Cuando el Gateway necesita
datos de otro microservicio, lo hace él mismo (nunca el microservicio
dueño del caso de uso):

- `POST/PUT /productos` → el Gateway valida contra `categoria-service`
  que la categoría exista (`ProductoOrquestador` + `CategoriaGatewayCliente`).
- `POST /ventas` → el Gateway valida contra `cliente-service` que el
  cliente exista, y contra `producto-service` que cada producto de la
  venta exista (`NotaVentaOrquestador` + `ClienteGatewayCliente` +
  `ProductoGatewayCliente`).
- `categoria-service` y `cliente-service` no dependen de nadie: son
  CRUD simple, sin orquestación.

## Estructura

```text
services/
  categoria-service/   # MS-Categoria, puerto 8085 - BD propia
  producto-service/     # MS-Producto, puerto 8086 - BD propia
  cliente-service/       # MS-Cliente, puerto 8087 - BD propia
  venta-service/          # MS-Venta (Nota_Venta + Vende), puerto 8088 - BD propia
  api-gateway/             # Punto de entrada unico, puerto 8080
frontend/                  # UI unica: Categorías, Productos, Clientes, Ventas
iniciar_todo.py            # Arranca los 5 procesos SIN Docker (ver mas abajo)
```

Cada microservicio tiene su propia base de datos (`CATEGORIA_DB_NAME`,
`PRODUCTO_DB_NAME`, `CLIENTE_DB_NAME`, `VENTA_DB_NAME` en `.env`) —
esto ya era así antes de agregar Cliente y Venta, y se mantiene igual:
una base de datos por microservicio, nunca compartida.

## Configuración

Copiar `.env.example` a `.env` en la raíz y completar los datos de
conexión de las 4 bases de datos. Antes de arrancar cada servicio hay
que haber creado su base de datos y corrido su `db/init.sql`:

```bash
psql -U postgres -c "CREATE DATABASE pos_tienda;"
psql -U postgres -d pos_tienda -f services/categoria-service/db/init.sql

psql -U postgres -c "CREATE DATABASE tienda_productos;"
psql -U postgres -d tienda_productos -f services/producto-service/db/init.sql

psql -U postgres -c "CREATE DATABASE tienda_clientes;"
psql -U postgres -d tienda_clientes -f services/cliente-service/db/init.sql

psql -U postgres -c "CREATE DATABASE tienda_ventas;"
psql -U postgres -d tienda_ventas -f services/venta-service/db/init.sql
```

## Cómo correr SIN Docker (recomendado para desarrollo/clase)

```bash
pip install psycopg2-binary
python iniciar_todo.py
```

`iniciar_todo.py` (raíz del proyecto, independiente de `services/`)
levanta el API-Gateway y los 4 microservicios como procesos Python
normales, cada uno leyendo su propia sección de `.env`, con logs
identificados por servicio en una sola consola. `Ctrl+C` los detiene
a todos ordenadamente. Luego, en otra terminal:

```bash
cd frontend
python -m http.server 3000
```

Abrir `http://localhost:3000`.

## Cómo correr manualmente (una terminal por proceso, sin el script)

```bash
python services/categoria-service/src/categoria_servidor.py
python services/producto-service/src/producto_servidor.py
python services/cliente-service/src/cliente_servidor.py
python services/venta-service/src/venta_servidor.py
python services/api-gateway/src/gateway_servidor.py
python -m http.server 3000   # desde frontend/
```

## Verificación rápida

```bash
curl http://localhost:8080/categorias
curl http://localhost:8080/productos
curl http://localhost:8080/clientes
curl http://localhost:8080/ventas
```

Un `POST http://localhost:8080/productos` con un `categoria_codigo`
inexistente debe responder `400` sin llegar a crear el producto; si
`categoria-service` está caído, debe responder `503`. Lo mismo aplica
a `POST /ventas` con un `cliente_ci` o `producto_codigo` inexistente.

