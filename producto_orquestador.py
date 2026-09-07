from categoria_gateway_cliente import CategoriaGatewayCliente, CategoriaServicioNoDisponible


class ProductoOrquestador:
    """Orquesta la validacion de categoria antes de crear/actualizar un
    producto. Reemplaza, a nivel de Gateway, la llamada directa que
    antes hacia MS-Producto a MS-Categoria: el Gateway si puede hablar
    con ambos servicios porque es la capa de orquestacion, no un
    microservicio par."""

    def __init__(self, categoria_cliente=None):
        self.categoria_cliente = categoria_cliente or CategoriaGatewayCliente()

    def validar_categoria_existente(self, categoria_codigo):
        """Devuelve (ok: bool, error: str|None).
        error en {"La categoria no existe.", "servicio_no_disponible"}"""
        try:
            existe = self.categoria_cliente.existe_categoria(categoria_codigo)
        except CategoriaServicioNoDisponible:
            return False, "servicio_no_disponible"

        if not existe:
            return False, "La categoria no existe."

        return True, None
