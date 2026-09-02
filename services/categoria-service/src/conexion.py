import os

import psycopg2


class Conexion:
    """Responsable unicamente de abrir la conexion a PostgreSQL.
    Corresponde a la clase 'Conexion' del detalle procedimental."""

    HOST = os.environ.get("CATEGORIA_DB_HOST", "localhost")
    PUERTO = int(os.environ.get("CATEGORIA_DB_PORT", 5432))
    BASE_DATOS = os.environ.get("CATEGORIA_DB_NAME", "pos_tienda")
    USUARIO = os.environ.get("CATEGORIA_DB_USER", "postgres")
    PASSWORD = os.environ.get("CATEGORIA_DB_PASSWORD", "")

    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=Conexion.HOST,
            port=Conexion.PUERTO,
            dbname=Conexion.BASE_DATOS,
            user=Conexion.USUARIO,
            password=Conexion.PASSWORD,
        )
