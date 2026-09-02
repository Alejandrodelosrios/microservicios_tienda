from http.server import HTTPServer

from producto_controller import ProductoController


# Puerto diferente al MS-Categoria (8085).
PUERTO = 8086


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
