from datetime import date

from notaventa_dao import NotaVentaDao
from entidad_nota_venta import NotaVenta
from entidad_vende import Vende


class NotaVentaN:
    """Capa NEGOCIO. Valida forma/tipo de los datos y calcula el monto
    total sumando cantidad*precio de cada item. NO valida que el cliente
    ni los productos existan: esa responsabilidad ya la cumplio el
    API-Gateway (notaventa_orquestador.py) ANTES de reenviar la
    peticion aqui. Esta clase nunca debe llamar a otro microservicio."""

    def __init__(self):
        self.dao = NotaVentaDao()

    def listar_venta(self):
        resultado = []
        for nota_venta in self.dao.listar():
            _nota, items = self.dao.obtener_por_nro(nota_venta.nro)
            resultado.append(nota_venta.to_dict(items))
        return resultado

    def obtener_venta(self, nro):
        nota_venta, items = self.dao.obtener_por_nro(nro)
        return nota_venta.to_dict(items) if nota_venta else None

    def _validar_items(self, items_entrada):
        if not isinstance(items_entrada, list) or len(items_entrada) == 0:
            return None, "La venta debe tener al menos un item."

        items = []
        for item in items_entrada:
            try:
                producto_codigo = int(item.get("producto_codigo"))
                cantidad = int(item.get("cantidad"))
                precio = float(item.get("precio"))
            except (TypeError, ValueError):
                return None, "Cada item necesita producto_codigo, cantidad y precio validos."

            if cantidad <= 0:
                return None, "La cantidad debe ser mayor a cero."
            if precio < 0:
                return None, "El precio no puede ser negativo."

            items.append(Vende(producto_codigo=producto_codigo, cantidad=cantidad, precio=precio))

        return items, None

    def crear_venta(self, cliente_ci, items_entrada, fecha=None):
        try:
            cliente_ci = int(cliente_ci)
        except (TypeError, ValueError):
            return {"ok": False, "error": "El cliente_ci debe ser un numero entero."}

        items, error = self._validar_items(items_entrada)
        if error:
            return {"ok": False, "error": error}

        monto = sum(item.cantidad * item.precio for item in items)
        nota_venta = NotaVenta(
            cliente_ci=cliente_ci,
            fecha=fecha or date.today().isoformat(),
            monto=monto,
        )

        self.dao.crear(nota_venta, items)
        return {"ok": True, "venta": nota_venta.to_dict(items)}
