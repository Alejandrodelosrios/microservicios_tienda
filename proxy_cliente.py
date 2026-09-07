from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ServicioDestinoNoDisponible(Exception):
    """El microservicio destino no respondio o no se pudo contactar."""
    pass


class ProxyCliente:
    """Reenvia una peticion HTTP a un microservicio destino usando urllib.
    Unico componente del Gateway que habla la red hacia los
    microservicios (ademas de CategoriaGatewayCliente para la
    orquestacion)."""

    @staticmethod
    def reenviar(metodo, base_url, ruta, cuerpo_bytes=None, timeout=5):
        url = f"{base_url}{ruta}"
        headers = {"Accept": "application/json"}
        if cuerpo_bytes is not None:
            headers["Content-Type"] = "application/json"

        request = Request(url, data=cuerpo_bytes, method=metodo, headers=headers)

        try:
            with urlopen(request, timeout=timeout) as respuesta:
                return respuesta.status, respuesta.read()
        except HTTPError as error:
            return error.code, error.read()
        except (URLError, TimeoutError) as error:
            raise ServicioDestinoNoDisponible(str(error))
