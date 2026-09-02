import os
from http.server import HTTPServer

from producto_controller import ProductoController


PUERTO = int(os.environ.get("PRODUCTO_SERVICE_PORT", 8086))


def main():
    servidor = HTTPServer(
        ("localhost", PUERTO),
        ProductoController,
    )

    print(
        "Microservicio de producto iniciado "
        f"en http://localhost:{PUERTO}"
    )

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        servidor.server_close()


if __name__ == "__main__":
    main()
