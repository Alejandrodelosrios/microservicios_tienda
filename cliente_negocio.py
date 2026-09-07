from cliente_dao import ClienteDao
from entidad_cliente import Cliente


class ClienteN:
    """Capa NEGOCIO. A diferencia de CategoriaN, aqui la unicidad del
    identificador (ci) se valida ANTES de insertar, porque no lo genera
    la base de datos (es una llave natural que trae el cliente)."""

    def __init__(self):
        self.dao = ClienteDao()

    def listar_cliente(self):
        return self.dao.listar()

    def obtener_cliente(self, ci):
        return self.dao.obtener_por_ci(ci)

    def _validar_datos(self, datos):
        """Valida forma/tipo de ci, nombre y telefono.
        Devuelve (ci, nombre, telefono, error)."""
        try:
            ci = int(datos.get("ci"))
        except (TypeError, ValueError):
            return None, None, None, "El ci debe ser un numero entero."

        nombre = (datos.get("nombre") or "").strip()
        if not nombre:
            return None, None, None, "El nombre no puede estar vacio."

        telefono = (datos.get("telefono") or "").strip()

        return ci, nombre, telefono, None

    def crear_cliente(self, datos):
        ci, nombre, telefono, error = self._validar_datos(datos)
        if error:
            return {"ok": False, "error": error}

        if self.dao.existe_ci(ci):
            return {"ok": False, "error": "Ya existe un cliente con ese ci."}

        cliente = Cliente(ci=ci, nombre=nombre, telefono=telefono)
        self.dao.crear(cliente)
        return {"ok": True, "cliente": cliente}

    def actualizar_cliente(self, ci_ruta, datos):
        datos = dict(datos)
        datos["ci"] = ci_ruta
        ci, nombre, telefono, error = self._validar_datos(datos)
        if error:
            return {"ok": False, "error": error}

        cliente = Cliente(ci=ci, nombre=nombre, telefono=telefono)
        actualizado = self.dao.actualizar(cliente)
        if not actualizado:
            return {"ok": False, "error": "El cliente no existe."}
        return {"ok": True, "cliente": cliente}

    def eliminar_cliente(self, ci):
        eliminado = self.dao.eliminar(ci)
        if not eliminado:
            return {"ok": False, "error": "El cliente no existe."}
        return {"ok": True}
