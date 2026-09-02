# API Gateway

Punto de entrada unico del sistema. Desarrollado con Python puro
(`http.server` + `urllib`), sin Flask/FastAPI/Django, para mantener el
mismo estilo que `categoria-service` y `producto-service`.

## Responsabilidades

- Es el **unico** componente que el frontend puede llamar.
- Enruta `/categorias*` hacia `categoria-service` y `/productos*` hacia
  `producto-service`.
- Centraliza CORS: `categoria-service` y `producto-service` ya no
  responden a peticiones de navegador.
- Orquesta la validacion de `categoria_codigo` antes de crear o
  actualizar un producto, llamando primero a `categoria-service`. Si la
  categoria no existe (o el servicio no responde), el Gateway responde
  el error y **nunca** reenvia la peticion a `producto-service`.

## Puerto

```text
http://localhost:8080
```

Configurable con `GATEWAY_PORT`. Las URLs de los microservicios
destino se configuran con `CATEGORIA_SERVICE_URL` y
`PRODUCTO_SERVICE_URL` (ver `.env.example` en la raíz del repo).

## Correr

```bash
python src/gateway_servidor.py
```

(desde `services/api-gateway`, con `categoria-service` y
`producto-service` ya en ejecución).
