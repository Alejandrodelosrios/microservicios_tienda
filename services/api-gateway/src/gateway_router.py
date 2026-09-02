import re

import config

RUTA_CATEGORIAS = re.compile(r"^/categorias(?:/(\d+))?$")
RUTA_PRODUCTOS = re.compile(r"^/productos(?:/(\d+))?$")


class GatewayRouter:
    """Resuelve a que microservicio pertenece una ruta entrante."""

    @staticmethod
    def resolver(path):
        if RUTA_CATEGORIAS.match(path):
            return config.CATEGORIA_SERVICE_URL, "categoria"
        if RUTA_PRODUCTOS.match(path):
            return config.PRODUCTO_SERVICE_URL, "producto"
        return None, None
