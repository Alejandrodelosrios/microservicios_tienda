from http.server import HTTPServer

import config
from gateway_controller import GatewayController


def main():
    servidor = HTTPServer(("0.0.0.0", config.GATEWAY_PORT), GatewayController)
    print(f"API Gateway iniciado en http://localhost:{config.GATEWAY_PORT}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        servidor.server_close()


if __name__ == "__main__":
    main()
