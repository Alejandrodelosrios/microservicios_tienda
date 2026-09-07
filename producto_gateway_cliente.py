import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import config


class ProductoServicioNoDisponible(Exception):
    """El MS-Producto no respondio o no se pudo contactar."""
    pass


class ProductoGatewayCliente:
    """Unico componente autorizado a preguntarle a MS-Producto si un
    codigo de producto existe. Se usa solo desde NotaVentaOrquestador
    (distinto de ProductoOrquestador, que valida categoria al crear un
    producto: aqui se valida producto al crear una venta)."""

    def __init__(self, base_url=None):
        self.base_url = (base_url or config.PRODUCTO_SERVICE_URL).rstrip("/")

    def existe_producto(self, codigo):
        url = f"{self.base_url}/productos/{codigo}"
        request = Request(url, method="GET", headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=5) as response:
                cuerpo = response.read().decode("utf-8")
                datos = json.loads(cuerpo)
                return isinstance(datos, dict) and bool(datos)
        except HTTPError as error:
            if error.code == 404:
                return False
            raise ProductoServicioNoDisponible(f"HTTP {error.code}")
        except (URLError, TimeoutError) as error:
            raise ProductoServicioNoDisponible(str(error))
        except (json.JSONDecodeError, ValueError):
            raise ProductoServicioNoDisponible("Respuesta invalida")
