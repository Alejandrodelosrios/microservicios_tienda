class NotaVenta:
    """Entidad pura (cabecera de la venta). Corresponde a 'Nota_Venta'
    del diagrama de dominio: nro, fecha, monto + FK cliente_ci."""

    def __init__(self, nro=None, cliente_ci=None, fecha=None, monto=None):
        self.nro = nro
        self.cliente_ci = cliente_ci
        self.fecha = fecha
        self.monto = monto

    def to_dict(self, items=None):
        return {
            "nro": self.nro,
            "cliente_ci": self.cliente_ci,
            "fecha": self.fecha,
            "monto": float(self.monto) if self.monto is not None else None,
            "items": [i.to_dict() for i in items] if items is not None else [],
        }

    @staticmethod
    def from_row(row):
        return NotaVenta(nro=row[0], cliente_ci=row[1], fecha=str(row[2]), monto=row[3])
