from conexion import Conexion
from entidad_categoria import Categoria


class CategoriaDao:
    """Capa DATOS: unico lugar que conoce SQL. Corresponde a CategoriaDao
    del detalle procedimental."""

    def crear(self, categoria):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO categoria (nombre) VALUES (%s) RETURNING codigo",
                    (categoria.nombre,),
                )
                categoria.codigo = cur.fetchone()[0]
            conn.commit()
            return True
        finally:
            conn.close()

    def obtener_por_id(self, codigo):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT codigo, nombre FROM categoria WHERE codigo = %s", (codigo,)
                )
                fila = cur.fetchone()
                return Categoria.from_row(fila) if fila else None
        finally:
            conn.close()

    def listar(self):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT codigo, nombre FROM categoria ORDER BY nombre")
                return [Categoria.from_row(fila) for fila in cur.fetchall()]
        finally:
            conn.close()

    def actualizar(self, categoria):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE categoria SET nombre = %s WHERE codigo = %s",
                    (categoria.nombre, categoria.codigo),
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
                cur.execute("DELETE FROM categoria WHERE codigo = %s", (codigo,))
                filas_afectadas = cur.rowcount
            conn.commit()
            return filas_afectadas > 0
        finally:
            conn.close()

    def existe_nombre(self, nombre, id_excluir=None):
        conn = Conexion.get_connection()
        try:
            with conn.cursor() as cur:
                if id_excluir:
                    cur.execute(
                        "SELECT 1 FROM categoria WHERE LOWER(nombre) = LOWER(%s) AND codigo != %s",
                        (nombre, id_excluir),
                    )
                else:
                    cur.execute(
                        "SELECT 1 FROM categoria WHERE LOWER(nombre) = LOWER(%s)",
                        (nombre,),
                    )
                return cur.fetchone() is not None
        finally:
            conn.close()
