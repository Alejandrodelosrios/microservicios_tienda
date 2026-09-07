import json
import re
from http.server import BaseHTTPRequestHandler

from cliente_negocio import ClienteN

negocio = ClienteN()
RUTA_CI = re.compile(r"^/clientes/(\d+)$")


class ClienteController(BaseHTTPRequestHandler):
    """Solo debe ser invocado por API-Gateway. No expone CORS: no esta
    pensado para ser llamado directamente desde el navegador."""

    def do_GET(self):
        if self.path == "/clientes":
            self.listar_cliente_handler()
            return
        match = RUTA_CI.match(self.path)
        if match:
            self.obtener_cliente_handler(int(match.group(1)))
        else:
            self.handler_error(404, "Ruta no encontrada")

    def do_POST(self):
        if self.path != "/clientes":
            self.handler_error(404, "Ruta no encontrada")
            return
        self.crear_cliente_handler(self._leer_cuerpo())

    def do_PUT(self):
        match = RUTA_CI.match(self.path)
        if not match:
            self.handler_error(404, "Ruta no encontrada")
            return
        self.actualizar_cliente_handler(int(match.group(1)), self._leer_cuerpo())

    def do_DELETE(self):
        match = RUTA_CI.match(self.path)
        if not match:
            self.handler_error(404, "Ruta no encontrada")
            return
        self.eliminar_cliente_handler(int(match.group(1)))

    # ---- Handlers: uno por accion ----

    def listar_cliente_handler(self):
        clientes = [c.to_dict() for c in negocio.listar_cliente()]
        self.send_response_json(200, clientes)

    def obtener_cliente_handler(self, ci):
        cliente = negocio.obtener_cliente(ci)
        if cliente:
            self.send_response_json(200, cliente.to_dict())
        else:
            self.handler_error(404, "Cliente no encontrado")

    def crear_cliente_handler(self, cuerpo):
        resultado = negocio.crear_cliente(cuerpo)
        if resultado["ok"]:
            self.send_response_json(201, resultado["cliente"].to_dict())
        else:
            self.handler_error(400, resultado["error"])

    def actualizar_cliente_handler(self, ci, cuerpo):
        resultado = negocio.actualizar_cliente(ci, cuerpo)
        if resultado["ok"]:
            self.send_response_json(200, resultado["cliente"].to_dict())
        else:
            codigo_http = 404 if "no existe" in resultado["error"] else 400
            self.handler_error(codigo_http, resultado["error"])

    def eliminar_cliente_handler(self, ci):
        resultado = negocio.eliminar_cliente(ci)
        if resultado["ok"]:
            self.send_response_json(200, {"mensaje": "Cliente eliminado"})
        else:
            self.handler_error(404, resultado["error"])

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
        print("[MS-Cliente] " + (formato % args))
