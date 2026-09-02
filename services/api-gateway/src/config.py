import os

GATEWAY_PORT = int(os.environ.get("GATEWAY_PORT", 8080))
CATEGORIA_SERVICE_URL = os.environ.get("CATEGORIA_SERVICE_URL", "http://localhost:8085").rstrip("/")
PRODUCTO_SERVICE_URL = os.environ.get("PRODUCTO_SERVICE_URL", "http://localhost:8086").rstrip("/")
CORS_ALLOWED_ORIGIN = os.environ.get("CORS_ALLOWED_ORIGIN", "*")
