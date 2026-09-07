from conexion import Conexion
from entidad_nota_venta import NotaVenta
from entidad_vende import Vende


class NotaVentaDao:
    """Capa DATOS. crear() inserta la cabecera (NotaVenta) y todas sus
    lineas (Vende) en UNA SOLA TRANSACCION: reflejan la composicion del
    diagrama de dominio (si se cae a mitad de camino, no debe quedar una
    nota de venta sin sus lineas, o viceversa)."""

    def crear(self, nota_venta, items_vende):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO nota_venta (cliente_ci, fecha, monto)
                    VALUES (%s, %s, %s)
                    RETURNING nro
                    """,
                    (nota_venta.cliente_ci, nota_venta.fecha, nota_venta.monto),
                )
                nota_venta.nro = cur.fetchone()[0]

                for item in items_vende:
                    item.nota_venta_nro = nota_venta.nro
                    cur.execute(
                        """
                        INSERT INTO vende
                            (nota_venta_nro, producto_codigo, cantidad, precio)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (item.nota_venta_nro, item.producto_codigo, item.cantidad, item.precio),
                    )
                    item.id = cur.fetchone()[0]

            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar(self):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT nro, cliente_ci, fecha, monto FROM nota_venta ORDER BY nro DESC"
                )
                return [NotaVenta.from_row(fila) for fila in cur.fetchall()]
        finally:
            conn.close()

    def obtener_por_nro(self, nro):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT nro, cliente_ci, fecha, monto FROM nota_venta WHERE nro = %s",
                    (nro,),
                )
                fila = cur.fetchone()
                if not fila:
                    return None, []
                nota_venta = NotaVenta.from_row(fila)

                cur.execute(
                    """
                    SELECT id, nota_venta_nro, producto_codigo, cantidad, precio
                    FROM vende WHERE nota_venta_nro = %s ORDER BY id
                    """,
                    (nro,),
                )
                items = [Vende.from_row(fila) for fila in cur.fetchall()]
                return nota_venta, items
        finally:
            conn.close()
