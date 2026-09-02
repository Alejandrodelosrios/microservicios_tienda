class Categoria:
    """Entidad pura: solo datos, sin logica de negocio ni de acceso a datos."""

    def __init__(self, codigo=None, nombre=None):
        self.codigo = codigo
        self.nombre = nombre

    def to_dict(self):
        return {"codigo": self.codigo, "nombre": self.nombre}

    @staticmethod
    def from_row(row):
        return Categoria(codigo=row[0], nombre=row[1])
