# Microservicios Tienda

Tienda basada en microservicios, desarrollada con Python puro
(`http.server`, sin Flask/FastAPI/Django) y un frontend estático en
HTML/CSS/JS sin frameworks ni build step.

## Arquitectura

```text
      Frontend (frontend/)
              |
              v
       API Gateway  :8080   (services/api-gateway)
         /        \
        v          v
Categoria-Service  Producto-Service
    :8085              :8086
(services/categoria-service) (services/producto-service)
```

Regla estricta: **el frontend solo llama al API Gateway, y los
microservicios nunca se llaman entre sí.** Cuando se crea o actualiza
un producto, es el API Gateway quien valida contra `categoria-service`
que la categoría exista antes de reenviar la petición a
`producto-service`; `producto-service` ya no conoce a `categoria-service`.

## Estructura

```text
services/
  categoria-service/   # MS-Categoria, puerto 8085
  producto-service/     # MS-Producto, puerto 8086
  api-gateway/           # Punto de entrada unico, puerto 8080
frontend/                # UI unica (Categorías + Productos)
```

## Configuración

Copiar `.env.example` y exportar las variables antes de arrancar cada
servicio (Windows PowerShell: `$env:VAR="valor"`; cmd: `set VAR=valor`).
Ninguna contraseña queda hardcodeada en el código.

## Cómo correr (en este orden, una terminal por proceso)

```bash
python services/categoria-service/src/categoria_servidor.py
python services/producto-service/src/producto_servidor.py
python services/api-gateway/src/gateway_servidor.py
python -m http.server 3000
```

El último comando debe ejecutarse desde `frontend/`. Luego abrir
`http://localhost:3000`.

## Verificación rápida

```bash
curl http://localhost:8080/categorias
curl http://localhost:8080/productos
```

Un `POST http://localhost:8080/productos` con un `categoria_codigo`
inexistente debe responder `400` sin llegar a crear el producto; si
`categoria-service` está caído, debe responder `503`.

## Cómo correr con Docker

Requiere Docker y Docker Compose. Un solo comando levanta las dos
bases de datos, los tres servicios y el frontend.

1. Copiar `.env.example` a `.env`. Trae `CATEGORIA_DB_PASSWORD` y
   `PRODUCTO_DB_PASSWORD` en `postgres` (valor de desarrollo local);
   cambialos antes de desplegar en un entorno accesible desde fuera —
   no pueden quedar vacios, la imagen de Postgres no arranca sin
   contraseña de superusuario.
2. `docker compose up -d --build`
3. Abrir `http://localhost:3000` (o el puerto de `FRONTEND_HOST_PORT`
   si lo cambiaste).

Si cambias `GATEWAY_HOST_PORT`, actualiza también `GATEWAY_PUBLIC_URL`
en `.env` — es el valor que usa el navegador, no se deduce
automáticamente del mapeo de puertos.

`categoria-service` y `producto-service` no publican puertos al host:
solo son alcanzables desde `api-gateway` a través de la red interna
de Docker.

### Verificación rápida (Docker)

```bash
curl http://localhost:8080/categorias
curl http://localhost:8080/productos
docker compose exec frontend cat /usr/share/nginx/html/js/config.js
curl http://localhost:8085/categorias   # debe fallar (connection refused)
curl http://localhost:8086/productos    # debe fallar (connection refused)
```
