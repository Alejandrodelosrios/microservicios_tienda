import os
from http.server import HTTPServer

from cliente_controller import ClienteController

PUERTO = int(os.environ.get("CLIENTE_SERVICE_PORT", 8087))


def main():
    servidor = HTTPServer(("0.0.0.0", PUERTO), ClienteController)
    print(f"Microservicio de cliente iniciado en http://localhost:{PUERTO}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        servidor.server_close()


if __name__ == "__main__":
    main()
