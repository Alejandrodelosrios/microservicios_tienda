import json
import re
from http.server import BaseHTTPRequestHandler

from categoria_negocio import CategoriaN

negocio = CategoriaN()
RUTA_ID = re.compile(r"^/categorias/(\d+)$")


class CategoriaController(BaseHTTPRequestHandler):
    """Solo debe ser invocado por API-Gateway. No expone CORS: no esta
    pensado para ser llamado directamente desde el navegador."""

    def do_GET(self):
        if self.path == "/categorias":
            self.listar_categoria_handler()
            return
        match = RUTA_ID.match(self.path)
        if match:
            self.obtener_categoria_handler(int(match.group(1)))
        else:
            self.handler_error(404, "Ruta no encontrada")

    def do_POST(self):
        if self.path != "/categorias":
            self.handler_error(404, "Ruta no encontrada")
            return
        self.crear_categoria_handler(self._leer_cuerpo())

    def do_PUT(self):
        match = RUTA_ID.match(self.path)
        if not match:
            self.handler_error(404, "Ruta no encontrada")
            return
        self.actualizar_categoria_handler(int(match.group(1)), self._leer_cuerpo())

    def do_DELETE(self):
        match = RUTA_ID.match(self.path)
        if not match:
            self.handler_error(404, "Ruta no encontrada")
            return
        self.eliminar_categoria_handler(int(match.group(1)))

    # ---- Handlers: uno por accion, alineados con
    #      MicroServicio_Categoria::Negocio::CategoriaController del diagrama ----

    def listar_categoria_handler(self):
        categorias = [c.to_dict() for c in negocio.listar_categoria()]
        self.send_response_json(200, categorias)

    def obtener_categoria_handler(self, codigo):
        categoria = negocio.obtener_categoria(codigo)
        if categoria:
            self.send_response_json(200, categoria.to_dict())
        else:
            self.handler_error(404, "Categoria no encontrada")

    def crear_categoria_handler(self, cuerpo):
        resultado = negocio.crear_categoria(cuerpo.get("nombre"))
        if resultado["ok"]:
            self.send_response_json(201, resultado["categoria"].to_dict())
        else:
            self.handler_error(400, resultado["error"])

    def actualizar_categoria_handler(self, codigo, cuerpo):
        resultado = negocio.actualizar_categoria(codigo, cuerpo.get("nombre"))
        if resultado["ok"]:
            self.send_response_json(200, resultado["categoria"].to_dict())
        else:
            codigo_http = 404 if "no existe" in resultado["error"] else 400
            self.handler_error(codigo_http, resultado["error"])

    def eliminar_categoria_handler(self, codigo):
        resultado = negocio.eliminar_categoria(codigo)
        if resultado["ok"]:
            self.send_response_json(200, {"mensaje": "Categoria eliminada"})
        else:
            self.handler_error(404, resultado["error"])

    # ---- Utilidades de respuesta (equivalen a sendResponse/handlerError del diagrama) ----
    # Nota: se usa "send_response_json" en vez de "sendResponse" porque
    # BaseHTTPRequestHandler ya reserva el nombre "send_response" para su propio uso interno.

    def send_response_json(self, codigo_http, data):
        cuerpo = json.dumps(data).encode("utf-8")
        self.send_response(codigo_http)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def handler_error(self, codigo_http, mensaje):
        self.send_response_json(codigo_http, {"error": mensaje})

    def _leer_cuerpo(self):
        largo = int(self.headers.get("Content-Length", 0))
        crudo = self.rfile.read(largo) if largo else b"{}"
        try:
            return json.loads(crudo)
        except json.JSONDecodeError:
            return {}

    def log_message(self, formato, *args):
        print("[MS-Categoria] " + (formato % args))
