import psycopg2


class Conexion:

    HOST = "localhost"
    PORT = 5432
    DATABASE = "tienda_productos"
    USER = "postgres"
    PASSWORD = "Rios1020"

    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=Conexion.HOST,
            port=Conexion.PORT,
            database=Conexion.DATABASE,
            user=Conexion.USER,
            password=Conexion.PASSWORD,
        )
