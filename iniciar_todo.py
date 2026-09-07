#!/usr/bin/env python3
"""
iniciar_todo.py
----------------------------------------------------------------------
Script INDEPENDIENTE (vive en la raiz del proyecto, fuera de services/)
que levanta el API-Gateway y los 4 microservicios SIN Docker: cada uno
como un proceso Python normal, cada uno con su propia base de datos
(las variables de entorno de cada servicio ya apuntan a una base de
datos distinta, ver .env.example).

Requisitos previos:
  1. Tener Postgres corriendo (local o remoto) y haber creado las 4
     bases de datos (una por microservicio) con su db/init.sql
     correspondiente:
       services/categoria-service/db/init.sql
       services/producto-service/db/init.sql
       services/cliente-service/db/init.sql
       services/venta-service/db/init.sql
  2. Copiar .env.example a .env en la raiz del proyecto y completar
     los datos de conexion (host, usuario, password, nombre de cada BD).
  3. pip install psycopg2-binary  (una sola vez, alcanza para todos
     los servicios porque todos son procesos del mismo interprete
     Python instalado en tu maquina).

Uso:
  python iniciar_todo.py            -> levanta los 5 procesos
  Ctrl+C                            -> los detiene a todos ordenadamente

Cada servicio corre en su propio proceso (no en threads), asi que un
crash de un microservicio no tumba a los demas ni al Gateway.
"""

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

# (nombre para los logs, carpeta del servicio, archivo que arranca el servidor)
SERVICIOS = [
    ("MS-Categoria", "services/categoria-service/src", "categoria_servidor.py"),
    ("MS-Producto",  "services/producto-service/src",  "producto_servidor.py"),
    ("MS-Cliente",   "services/cliente-service/src",   "cliente_servidor.py"),
    ("MS-Venta",     "services/venta-service/src",     "venta_servidor.py"),
    ("API-Gateway",  "services/api-gateway/src",        "gateway_servidor.py"),
]

COLORES = ["\033[36m", "\033[35m", "\033[33m", "\033[32m", "\033[34m"]
RESET = "\033[0m"


def cargar_env_file(ruta_env):
    """Lee un archivo .env simple (CLAVE=valor por linea) sin depender
    de python-dotenv (el proyecto no tiene dependencias externas mas
    alla de psycopg2-binary)."""
    variables = {}
    if not ruta_env.exists():
        return variables
    for linea in ruta_env.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        variables[clave.strip()] = valor.strip()
    return variables


def imprimir_con_prefijo(proceso, nombre, color):
    for linea in proceso.stdout:
        print(f"{color}[{nombre}]{RESET} {linea}", end="")


def main():
    env_archivo = cargar_env_file(RAIZ / ".env")
    if not env_archivo:
        print(
            "AVISO: no se encontro un archivo .env en la raiz del proyecto.\n"
            "       Copia .env.example a .env y completa los datos de conexion\n"
            "       de las 4 bases de datos antes de continuar (si no, cada\n"
            "       servicio usara los valores por defecto de su conexion.py).\n"
        )

    entorno = {**os.environ, **env_archivo}

    procesos = []
    hilos = []

    print("Levantando API-Gateway + 4 microservicios (sin Docker)...\n")

    for i, (nombre, carpeta, archivo) in enumerate(SERVICIOS):
        color = COLORES[i % len(COLORES)]
        cwd = RAIZ / carpeta
        proceso = subprocess.Popen(
            [sys.executable, archivo],
            cwd=str(cwd),
            env=entorno,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        procesos.append((nombre, proceso))

        hilo = threading.Thread(
            target=imprimir_con_prefijo, args=(proceso, nombre, color), daemon=True
        )
        hilo.start()
        hilos.append(hilo)

        # Pequeña espera entre arranques para que los logs no se
        # entremezclen justo al inicio (puramente cosmetico).
        time.sleep(0.3)

    def detener_todo(*_args):
        print("\nDeteniendo todos los servicios...")
        for nombre, proceso in procesos:
            if proceso.poll() is None:
                proceso.send_signal(signal.SIGINT)
        for nombre, proceso in procesos:
            try:
                proceso.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proceso.kill()
        print("Todos los servicios se detuvieron.")
        sys.exit(0)

    signal.signal(signal.SIGINT, detener_todo)
    signal.signal(signal.SIGTERM, detener_todo)

    print(
        "\nListo. Endpoints por defecto:\n"
        "  API-Gateway:   http://localhost:8080\n"
        "  MS-Categoria:  http://localhost:8085 (uso interno del Gateway)\n"
        "  MS-Producto:   http://localhost:8086 (uso interno del Gateway)\n"
        "  MS-Cliente:    http://localhost:8087 (uso interno del Gateway)\n"
        "  MS-Venta:      http://localhost:8088 (uso interno del Gateway)\n"
        "\nAbre frontend/index.html en el navegador (o sirvelo con un\n"
        "servidor estatico) para usar la interfaz. Ctrl+C aqui detiene todo.\n"
    )

    # Si algun proceso muere solo (crash), lo reportamos pero dejamos
    # los demas corriendo, salvo que sea el Gateway (sin el, nada funciona).
    while True:
        time.sleep(1)
        for nombre, proceso in procesos:
            codigo = proceso.poll()
            if codigo is not None:
                print(f"\n[{nombre}] se detuvo (codigo {codigo}).")
                if nombre == "API-Gateway":
                    detener_todo()
                procesos.remove((nombre, proceso))
                break


if __name__ == "__main__":
    main()
