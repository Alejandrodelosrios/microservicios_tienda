from cliente_gateway_cliente import ClienteGatewayCliente, ClienteServicioNoDisponible
from producto_gateway_cliente import ProductoGatewayCliente, ProductoServicioNoDisponible


class NotaVentaOrquestador:
    """Orquesta la validacion de cliente y de cada producto ANTES de
    crear una venta. Es el unico punto del sistema con permiso para
    hablar con dos microservicios distintos en la misma operacion."""

    def __init__(self, cliente_cliente=None, producto_cliente=None):
        self.cliente_cliente = cliente_cliente or ClienteGatewayCliente()
        self.producto_cliente = producto_cliente or ProductoGatewayCliente()

    def validar_venta(self, cliente_ci, items):
        """Devuelve (ok: bool, error: str|None)."""
        try:
            existe_cliente = self.cliente_cliente.existe_cliente(cliente_ci)
        except ClienteServicioNoDisponible:
            return False, "servicio_no_disponible"

        if not existe_cliente:
            return False, "El cliente no existe."

        for item in items or []:
            codigo = item.get("producto_codigo")
            try:
                existe_producto = self.producto_cliente.existe_producto(codigo)
            except ProductoServicioNoDisponible:
                return False, "servicio_no_disponible"

            if not existe_producto:
                return False, f"El producto {codigo} no existe."

        return True, None
