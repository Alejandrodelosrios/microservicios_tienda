import re

import config

RUTA_CATEGORIAS = re.compile(r"^/categorias(?:/(\d+))?$")
RUTA_PRODUCTOS = re.compile(r"^/productos(?:/(\d+))?$")
RUTA_CLIENTES = re.compile(r"^/clientes(?:/(\d+))?$")
RUTA_VENTAS = re.compile(r"^/ventas(?:/(\d+))?$")


class GatewayRouter:
    """Resuelve a que microservicio pertenece una ruta entrante."""

    @staticmethod
    def resolver(path):
        if RUTA_CATEGORIAS.match(path):
            return config.CATEGORIA_SERVICE_URL, "categoria"
        if RUTA_PRODUCTOS.match(path):
            return config.PRODUCTO_SERVICE_URL, "producto"
        if RUTA_CLIENTES.match(path):
            return config.CLIENTE_SERVICE_URL, "cliente"
        if RUTA_VENTAS.match(path):
            return config.VENTA_SERVICE_URL, "venta"
        return None, None
