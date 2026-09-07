import os
from http.server import HTTPServer

from notaventa_controller import NotaVentaController

PUERTO = int(os.environ.get("VENTA_SERVICE_PORT", 8088))


def main():
    servidor = HTTPServer(("0.0.0.0", PUERTO), NotaVentaController)
    print(f"Microservicio de venta iniciado en http://localhost:{PUERTO}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        servidor.server_close()


if __name__ == "__main__":
    main()
