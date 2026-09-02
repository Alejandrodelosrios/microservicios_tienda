import os

import psycopg2


class Conexion:

    HOST = os.environ.get("PRODUCTO_DB_HOST", "localhost")
    PORT = int(os.environ.get("PRODUCTO_DB_PORT", 5432))
    DATABASE = os.environ.get("PRODUCTO_DB_NAME", "tienda_productos")
    USER = os.environ.get("PRODUCTO_DB_USER", "postgres")
    PASSWORD = os.environ.get("PRODUCTO_DB_PASSWORD", "")

    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=Conexion.HOST,
            port=Conexion.PORT,
            database=Conexion.DATABASE,
            user=Conexion.USER,
            password=Conexion.PASSWORD,
        )
