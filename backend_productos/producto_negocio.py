from producto_dao import ProductoDao
from entidad_producto import Producto
from categoria_client import CategoriaClient, CategoriaServicioNoDisponible


class ProductoN:
    """
    Capa NEGOCIO.

    Coordina ProductoDao con CategoriaClient para validar
    que la categoria exista antes de crear o actualizar.
    """

    def __init__(self):
        self.dao = ProductoDao()
        self.categoriaClient = CategoriaClient()

    def listarProducto(self):
        return self.dao.listar()

    def obtenerProducto(self, codigo):
        return self.dao.obtener_por_codigo(codigo)

    def _validar_datos(self, prod):
        """Valida nombre, precio y categoria. Devuelve (nombre, precio, categoria_codigo, error)."""
        nombre = (prod.get("nombre") or "").strip()
        precio = prod.get("precio")
        categoria_codigo = prod.get("categoria_codigo")

        if not nombre:
            return None, None, None, "El nombre del producto no puede estar vacio."

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            return None, None, None, "El precio debe ser un numero valido."

        if precio < 0:
            return None, None, None, "El precio no puede ser negativo."

        try:
            categoria_codigo = int(categoria_codigo)
        except (TypeError, ValueError):
            return None, None, None, "La categoria_codigo debe ser un numero entero."

        try:
            existe = self.categoriaClient.existeCategoria(categoria_codigo)
        except CategoriaServicioNoDisponible:
            return None, None, None, "servicio_no_disponible"

        if not existe:
            return None, None, None, "La categoria no existe."

        return nombre, precio, categoria_codigo, None

    def crearProducto(self, prod):
        nombre, precio, categoria_codigo, error = self._validar_datos(prod)

        if error:
            return {"ok": False, "error": error}

        producto = Producto(
            nombre=nombre,
            precio=precio,
            categoria_codigo=categoria_codigo,
        )

        self.dao.crear(producto)

        return {"ok": True, "producto": producto}

    def actualizarProducto(self, prod):
        try:
            codigo = int(prod.get("codigo"))
        except (TypeError, ValueError):
            return {"ok": False, "error": "El codigo del producto no es valido."}

        nombre, precio, categoria_codigo, error = self._validar_datos(prod)

        if error:
            return {"ok": False, "error": error}

        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            categoria_codigo=categoria_codigo,
        )

        actualizado = self.dao.actualizar(producto)

        if not actualizado:
            return {"ok": False, "error": "El producto no existe."}

        return {"ok": True, "producto": producto}

    def eliminarProducto(self, codigo):
        eliminado = self.dao.eliminar(codigo)

        if not eliminado:
            return {"ok": False, "error": "El producto no existe."}

        return {"ok": True}