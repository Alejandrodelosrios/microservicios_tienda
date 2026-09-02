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
