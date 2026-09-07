import json
import re
from http.server import BaseHTTPRequestHandler

from notaventa_negocio import NotaVentaN

negocio = NotaVentaN()
RUTA_NRO = re.compile(r"^/ventas/(\d+)$")


class NotaVentaController(BaseHTTPRequestHandler):
    """Solo debe ser invocado por API-Gateway. No expone CORS."""

    def do_GET(self):
        if self.path == "/ventas":
            self.listar_venta_handler()
            return
        match = RUTA_NRO.match(self.path)
        if match:
            self.obtener_venta_handler(int(match.group(1)))
        else:
            self.handler_error(404, "Ruta no encontrada")

    def do_POST(self):
        if self.path != "/ventas":
            self.handler_error(404, "Ruta no encontrada")
            return
        self.crear_venta_handler(self._leer_cuerpo())

    # ---- Handlers ----

    def listar_venta_handler(self):
        self.send_response_json(200, negocio.listar_venta())

    def obtener_venta_handler(self, nro):
        venta = negocio.obtener_venta(nro)
        if venta:
            self.send_response_json(200, venta)
        else:
            self.handler_error(404, "Venta no encontrada")

    def crear_venta_handler(self, cuerpo):
        resultado = negocio.crear_venta(
            cuerpo.get("cliente_ci"),
            cuerpo.get("items", []),
            cuerpo.get("fecha"),
        )
        if resultado["ok"]:
            self.send_response_json(201, resultado["venta"])
        else:
            self.handler_error(400, resultado["error"])

    # ---- Utilidades de respuesta ----

    def send_response_json(self, codigo_http, data):
        cuerpo = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo_http)
        self.send_header("Content-Type", "application/json; charset=utf-8")
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
        print("[MS-Venta] " + (formato % args))
