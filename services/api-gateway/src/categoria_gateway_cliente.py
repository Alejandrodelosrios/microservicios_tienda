import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import config


class CategoriaServicioNoDisponible(Exception):
    """El MS-Categoria no respondio o no se pudo contactar."""
    pass


class CategoriaGatewayCliente:
    """Unico componente de todo el sistema autorizado a preguntarle a
    MS-Categoria si un codigo de categoria existe. Vive en el
    API-Gateway porque es la capa de orquestacion, no un microservicio
    par de MS-Producto (antes esta clase vivia en MS-Producto como
    CategoriaClient; ese acoplamiento directo entre microservicios
    quedo prohibido)."""

    def __init__(self, base_url=None):
        self.base_url = (base_url or config.CATEGORIA_SERVICE_URL).rstrip("/")

    def existe_categoria(self, codigo):
        url = f"{self.base_url}/categorias/{codigo}"
        request = Request(url, method="GET", headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=5) as response:
                cuerpo = response.read().decode("utf-8")
                datos = json.loads(cuerpo)
                return isinstance(datos, dict) and bool(datos)
        except HTTPError as error:
            if error.code == 404:
                return False
            raise CategoriaServicioNoDisponible(f"HTTP {error.code}")
        except (URLError, TimeoutError) as error:
            raise CategoriaServicioNoDisponible(str(error))
        except (json.JSONDecodeError, ValueError):
            raise CategoriaServicioNoDisponible("Respuesta invalida")
