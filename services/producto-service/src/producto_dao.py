from conexion import Conexion
from entidad_producto import Producto


class ProductoDao:
    def crear(self, producto):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO producto
                        (nombre, precio, categoria_codigo)
                    VALUES
                        (%s, %s, %s)
                    RETURNING codigo
                    """,
                    (
                        producto.nombre,
                        producto.precio,
                        producto.categoria_codigo,
                    ),
                )
                producto.codigo = cur.fetchone()[0]

            conn.commit()
            return True
        finally:
            conn.close()

    def obtener_por_codigo(self, codigo):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT codigo, nombre, precio, categoria_codigo
                    FROM producto
                    WHERE codigo = %s
                    """,
                    (codigo,),
                )

                fila = cur.fetchone()
                return Producto.from_row(fila) if fila else None
        finally:
            conn.close()

    def listar(self):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT codigo, nombre, precio, categoria_codigo
                    FROM producto
                    ORDER BY nombre
                    """
                )

                return [
                    Producto.from_row(fila)
                    for fila in cur.fetchall()
                ]
        finally:
            conn.close()

    def actualizar(self, producto):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE producto
                    SET nombre = %s,
                        precio = %s,
                        categoria_codigo = %s
                    WHERE codigo = %s
                    """,
                    (
                        producto.nombre,
                        producto.precio,
                        producto.categoria_codigo,
                        producto.codigo,
                    ),
                )

                filas_afectadas = cur.rowcount

            conn.commit()
            return filas_afectadas > 0
        finally:
            conn.close()

    def eliminar(self, codigo):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM producto WHERE codigo = %s",
                    (codigo,),
                )

                filas_afectadas = cur.rowcount

            conn.commit()
            return filas_afectadas > 0
        finally:
            conn.close()
