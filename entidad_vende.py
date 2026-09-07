class Vende:
    """Entidad pura (detalle de la venta / linea de producto). Corresponde
    a 'Vende' del diagrama de dominio: id, precio, cantidad + FKs
    nota_venta_nro y producto_codigo. 'precio' aqui es el precio AL
    MOMENTO DE LA VENTA (una foto historica), no el precio actual del
    Producto en MS-Producto."""

    def __init__(self, id=None, nota_venta_nro=None, producto_codigo=None, cantidad=None, precio=None):
        self.id = id
        self.nota_venta_nro = nota_venta_nro
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        return {
            "id": self.id,
            "nota_venta_nro": self.nota_venta_nro,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "precio": float(self.precio) if self.precio is not None else None,
        }

    @staticmethod
    def from_row(row):
        return Vende(
            id=row[0],
            nota_venta_nro=row[1],
            producto_codigo=row[2],
            cantidad=row[3],
            precio=row[4],
        )
