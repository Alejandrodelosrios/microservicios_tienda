import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import config


class ClienteServicioNoDisponible(Exception):
    """El MS-Cliente no respondio o no se pudo contactar."""
    pass


class ClienteGatewayCliente:
    """Unico componente autorizado a preguntarle a MS-Cliente si un ci
    existe. Vive en el API-Gateway (capa de orquestacion), igual que
    CategoriaGatewayCliente. No usa GatewayRouter: ya sabe exactamente
    a que microservicio le habla, GatewayRouter solo resuelve a donde
    reenviar la peticion ORIGINAL del navegador."""

    def __init__(self, base_url=None):
        self.base_url = (base_url or config.CLIENTE_SERVICE_URL).rstrip("/")

    def existe_cliente(self, ci):
        url = f"{self.base_url}/clientes/{ci}"
        request = Request(url, method="GET", headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=5) as response:
                cuerpo = response.read().decode("utf-8")
                datos = json.loads(cuerpo)
                return isinstance(datos, dict) and bool(datos)
        except HTTPError as error:
            if error.code == 404:
                return False
            raise ClienteServicioNoDisponible(f"HTTP {error.code}")
        except (URLError, TimeoutError) as error:
            raise ClienteServicioNoDisponible(str(error))
        except (json.JSONDecodeError, ValueError):
            raise ClienteServicioNoDisponible("Respuesta invalida")
