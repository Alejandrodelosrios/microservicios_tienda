class Producto:
    """Entidad pura: solo datos, sin logica de negocio ni de acceso a datos."""

    def __init__(self, codigo=None, nombre=None, precio=None, categoria_codigo=None):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria_codigo = categoria_codigo

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": float(self.precio) if self.precio is not None else None,
            "categoria_codigo": self.categoria_codigo,
        }

    @staticmethod
    def from_row(row):
        return Producto(
            codigo=row[0],
            nombre=row[1],
            precio=row[2],
            categoria_codigo=row[3],
        )

    def getCodigo(self):
        return self.codigo

    def getNombre(self):
        return self.nombre

    def getPrecio(self):
        return self.precio

    def getcategoria_codigo(self):
        return self.categoria_codigo

    def setCodigo(self, valor):
        self.codigo = valor

    def setNombre(self, valor):
        self.nombre = valor

    def setPrecio(self, valor):
        self.precio = valor

    def setcategoria_codigo(self, valor):
        self.categoria_codigo = valor
