import json
import re
from http.server import BaseHTTPRequestHandler

from producto_negocio import ProductoN


negocio = ProductoN()
RUTA_ID = re.compile(r"^/productos/(\d+)$")


class ProductoController(BaseHTTPRequestHandler):
    """Solo debe ser invocado por API-Gateway. No expone CORS: no esta
    pensado para ser llamado directamente desde el navegador."""

    def _mapear_codigo_http(self, error):
        if "no existe" in error:
            return 404
        return 400

    def do_GET(self):
        if self.path == "/productos":
            self.listarProductoHandler()
            return

        match = RUTA_ID.match(self.path)

        if match:
            self.obtenerProductoHandler(int(match.group(1)))
        else:
            self.handlerError(404, "Ruta no encontrada")

    def do_POST(self):
        if self.path != "/productos":
            self.handlerError(404, "Ruta no encontrada")
            return

        self.crearProductoHandler(self._leer_cuerpo())

    def do_PUT(self):
        match = RUTA_ID.match(self.path)

        if not match:
            self.handlerError(404, "Ruta no encontrada")
            return

        cuerpo = self._leer_cuerpo()
        cuerpo["codigo"] = int(match.group(1))

        self.actualizarProductoHandler(cuerpo)

    def do_DELETE(self):
        match = RUTA_ID.match(self.path)

        if not match:
            self.handlerError(404, "Ruta no encontrada")
            return

        self.eliminarProductoHandler(int(match.group(1)))

    # ---- Handlers: uno por accion, alineados con
    #      Negocio::ProductoController del diagrama ----

    def listarProductoHandler(self):
        productos = [
            p.to_dict()
            for p in negocio.listarProducto()
        ]

        self.sendResponseJson(200, productos)

    def obtenerProductoHandler(self, codigo):
        producto = negocio.obtenerProducto(codigo)

        if producto:
            self.sendResponseJson(
                200,
                producto.to_dict(),
            )
        else:
            self.handlerError(
                404,
                "Producto no encontrado",
            )

    def crearProductoHandler(self, cuerpo):
        resultado = negocio.crearProducto(cuerpo)

        if resultado["ok"]:
            self.sendResponseJson(201, resultado["producto"].to_dict())
        else:
            self.handlerError(self._mapear_codigo_http(resultado["error"]), resultado["error"])

    def actualizarProductoHandler(self, cuerpo):
        resultado = negocio.actualizarProducto(cuerpo)

        if resultado["ok"]:
            self.sendResponseJson(
                200,
                resultado["producto"].to_dict(),
            )
        else:
            self.handlerError(self._mapear_codigo_http(resultado["error"]), resultado["error"])

    def eliminarProductoHandler(self, codigo):
        resultado = negocio.eliminarProducto(codigo)

        if resultado["ok"]:
            self.sendResponseJson(
                200,
                {"mensaje": "Producto eliminado"},
            )
        else:
            self.handlerError(
                404,
                resultado["error"],
            )

    # ---- Utilidades de respuesta (equivalen a sendResponse/handlerError del diagrama) ----
    # Nota: se usa "sendResponseJson" en vez de "sendResponse" porque
    # BaseHTTPRequestHandler ya reserva el nombre "send_response" para su propio uso interno.

    def sendResponseJson(self, codigo_http, data):
        cuerpo = json.dumps(
            data,
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(codigo_http)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(cuerpo)),
        )

        self.end_headers()
        self.wfile.write(cuerpo)

    def handlerError(self, codigo_http, mensaje):
        self.sendResponseJson(
            codigo_http,
            {"error": mensaje},
        )

    def _leer_cuerpo(self):
        largo = int(
            self.headers.get(
                "Content-Length",
                0,
            )
        )

        crudo = (
            self.rfile.read(largo)
            if largo
            else b"{}"
        )

        try:
            return json.loads(
                crudo.decode("utf-8")
            )
        except (
            json.JSONDecodeError,
            UnicodeDecodeError,
        ):
            return {}

    def log_message(self, formato, *args):
        print(
            "[MS-Producto] "
            + (formato % args)
        )
