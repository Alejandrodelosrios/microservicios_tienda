from conexion import Conexion
from entidad_cliente import Cliente


class ClienteDao:
    """Capa DATOS: unico lugar que conoce SQL."""

    def crear(self, cliente):
        # A diferencia de CategoriaDao.crear(), aqui NO hay
        # "RETURNING codigo": el ci lo trae el cliente ya armado
        # (llave natural, no autogenerada).
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO cliente (ci, nombre, telefono) VALUES (%s, %s, %s)",
                    (cliente.ci, cliente.nombre, cliente.telefono),
                )
            conn.commit()
            return True
        finally:
            conn.close()

    def obtener_por_ci(self, ci):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT ci, nombre, telefono FROM cliente WHERE ci = %s", (ci,)
                )
                fila = cur.fetchone()
                return Cliente.from_row(fila) if fila else None
        finally:
            conn.close()

    def listar(self):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT ci, nombre, telefono FROM cliente ORDER BY nombre")
                return [Cliente.from_row(fila) for fila in cur.fetchall()]
        finally:
            conn.close()

    def actualizar(self, cliente):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE cliente SET nombre = %s, telefono = %s WHERE ci = %s",
                    (cliente.nombre, cliente.telefono, cliente.ci),
                )
                filas_afectadas = cur.rowcount
            conn.commit()
            return filas_afectadas > 0
        finally:
            conn.close()

    def eliminar(self, ci):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM cliente WHERE ci = %s", (ci,))
                filas_afectadas = cur.rowcount
            conn.commit()
            return filas_afectadas > 0
        finally:
            conn.close()

    def existe_ci(self, ci):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM cliente WHERE ci = %s", (ci,))
                return cur.fetchone() is not None
        finally:
            conn.close()
