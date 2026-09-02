import os
from http.server import HTTPServer

from categoria_controller import CategoriaController

PUERTO = int(os.environ.get("CATEGORIA_SERVICE_PORT", 8085))


def main():
    servidor = HTTPServer(("localhost", PUERTO), CategoriaController)
    print(f"Microservicio de categoria iniciado en http://localhost:{PUERTO}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        servidor.server_close()


if __name__ == "__main__":
    main()
