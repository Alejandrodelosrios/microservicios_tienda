from categoria_dao import CategoriaDao
from entidad_categoria import Categoria


class CategoriaN:

    def __init__(self):
        self.dao = CategoriaDao()

    def listar_categoria(self):
        return self.dao.listar()

    def obtener_categoria(self, codigo):
        return self.dao.obtener_por_id(codigo)

    def crear_categoria(self, nombre):
        nombre = (nombre or "").strip()
        if not nombre:
            return {"ok": False, "error": "El nombre de la categoria no puede estar vacio."}
        if self.dao.existe_nombre(nombre):
            return {"ok": False, "error": "Ya existe una categoria con ese nombre."}

        categoria = Categoria(nombre=nombre)
        self.dao.crear(categoria)
        return {"ok": True, "categoria": categoria}

    def actualizar_categoria(self, codigo, nombre):
        nombre = (nombre or "").strip()
        if not nombre:
            return {"ok": False, "error": "El nombre de la categoria no puede estar vacio."}
        if self.dao.existe_nombre(nombre, id_excluir=codigo):
            return {"ok": False, "error": "Ya existe una categoria con ese nombre."}

        categoria = Categoria(codigo=codigo, nombre=nombre)
        actualizado = self.dao.actualizar(categoria)
        if not actualizado:
            return {"ok": False, "error": "La categoria no existe."}
        return {"ok": True, "categoria": categoria}

    def eliminar_categoria(self, codigo):
        eliminado = self.dao.eliminar(codigo)
        if not eliminado:
            return {"ok": False, "error": "La categoria no existe."}
        return {"ok": True}
