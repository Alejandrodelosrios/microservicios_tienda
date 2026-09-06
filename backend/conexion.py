import psycopg2


class Conexion:
    """Responsable unicamente de abrir la conexion a PostgreSQL.
    Corresponde a la clase 'Conexion' del detalle procedimental."""

    HOST = "localhost"
    PUERTO = 5432
    BASE_DATOS = "pos_tienda"
    USUARIO = "postgres"
    PASSWORD = "Rios1020"

    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=Conexion.HOST,
            port=Conexion.PUERTO,
            dbname=Conexion.BASE_DATOS,
            user=Conexion.USUARIO,
            password=Conexion.PASSWORD,
        )
