import json
import re
from http.server import BaseHTTPRequestHandler

import config
from gateway_router import GatewayRouter
from proxy_cliente import ProxyCliente, ServicioDestinoNoDisponible
from producto_orquestador import ProductoOrquestador

RUTA_PRODUCTOS = re.compile(r"^/productos(?:/(\d+))?$")

orquestador = ProductoOrquestador()


class GatewayController(BaseHTTPRequestHandler):
    """Unico punto de entrada HTTP del sistema para el frontend.
    Enruta y reenvia las peticiones a los microservicios via
    ProxyCliente; los microservicios nunca se llaman entre si."""

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", config.CORS_ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self._proxy_simple("GET")

    def do_DELETE(self):
        self._proxy_simple("DELETE")

    def do_POST(self):
        if RUTA_PRODUCTOS.match(self.path):
            self._proxy_producto_con_orquestacion("POST")
        else:
            self._proxy_simple("POST")

    def do_PUT(self):
        if RUTA_PRODUCTOS.match(self.path):
            self._proxy_producto_con_orquestacion("PUT")
        else:
            self._proxy_simple("PUT")

    # ---- Passthrough puro (GET/DELETE y todo lo que no sea /productos) ----

    def _proxy_simple(self, metodo):
        base_url, _dominio = GatewayRouter.resolver(self.path)

        if not base_url:
            self.handler_error(404, "Ruta no encontrada")
            return

        cuerpo_bytes = self._leer_cuerpo_bytes() if metodo in ("POST", "PUT") else None

        try:
            status, cuerpo_respuesta = ProxyCliente.reenviar(metodo, base_url, self.path, cuerpo_bytes)
        except ServicioDestinoNoDisponible:
            self.handler_error(503, "servicio_no_disponible")
            return

        self._reenviar_respuesta(status, cuerpo_respuesta)

    # ---- Passthrough con orquestacion de categoria (POST/PUT /productos) ----

    def _proxy_producto_con_orquestacion(self, metodo):
        cuerpo_bytes = self._leer_cuerpo_bytes()
        cuerpo = self._parsear_cuerpo_entrante(cuerpo_bytes)

        categoria_codigo_int = self._a_entero(cuerpo.get("categoria_codigo"))

        if categoria_codigo_int is not None:
            ok, error = orquestador.validar_categoria_existente(categoria_codigo_int)
            if not ok:
                self.handler_error(self._mapear_codigo_orquestacion(error), error)
                return

        try:
            status, cuerpo_respuesta = ProxyCliente.reenviar(
                metodo, config.PRODUCTO_SERVICE_URL, self.path, cuerpo_bytes
            )
        except ServicioDestinoNoDisponible:
            self.handler_error(503, "servicio_no_disponible")
            return

        self._reenviar_respuesta(status, cuerpo_respuesta)

    def _mapear_codigo_orquestacion(self, error):
        return 503 if error == "servicio_no_disponible" else 400

    @staticmethod
    def _a_entero(valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return None

    # ---- Utilidades de respuesta ----

    def _reenviar_respuesta(self, status, cuerpo_bytes):
        try:
            datos = json.loads(cuerpo_bytes.decode("utf-8")) if cuerpo_bytes else None
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.handler_error(502, "respuesta_invalida_del_servicio")
            return
        self.send_response_json(status, datos)

    def send_response_json(self, codigo_http, data):
        cuerpo = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo_http)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", config.CORS_ALLOWED_ORIGIN)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def handler_error(self, codigo_http, mensaje):
        self.send_response_json(codigo_http, {"error": mensaje})

    def _leer_cuerpo_bytes(self):
        largo = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(largo) if largo else b"{}"

    def _parsear_cuerpo_entrante(self, cuerpo_bytes):
        try:
            datos = json.loads(cuerpo_bytes.decode("utf-8"))
            return datos if isinstance(datos, dict) else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def log_message(self, formato, *args):
        print("[API-Gateway] " + (formato % args))
