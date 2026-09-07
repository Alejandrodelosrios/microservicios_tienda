class Cliente:
    """Entidad pura: solo datos, sin logica de negocio ni de acceso a datos.
    A diferencia de Categoria/Producto, 'ci' NO se autogenera: es la
    cedula/carnet del cliente, la anota el usuario en el formulario."""

    def __init__(self, ci=None, nombre=None, telefono=None):
        self.ci = ci
        self.nombre = nombre
        self.telefono = telefono

    def to_dict(self):
        return {"ci": self.ci, "nombre": self.nombre, "telefono": self.telefono}

    @staticmethod
    def from_row(row):
        return Cliente(ci=row[0], nombre=row[1], telefono=row[2])
