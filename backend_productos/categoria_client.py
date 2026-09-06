import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class CategoriaServicioNoDisponible(Exception):
    """El MS-Categoria no respondió o no se pudo contactar."""
    pass


class CategoriaClient:

    def __init__(self, base_url=None):
        self.base_url = (
            base_url or os.getenv("CATEGORIA_URL", "http://localhost:8085")
        ).rstrip("/")

    def existeCategoria(self, codigo):
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