class CategoriaControladorUI {
  constructor() {
    this.gateway = new ApiGateway();
    this.adapter = new CategoriaAdapter(document.querySelector("#tabla-categorias tbody"));
    this.inputNombre = document.querySelector("#input-nombre");
    this.inputBusqueda = document.querySelector("#input-busqueda");
    this.seleccionada = null;
    this.categoriasCompletas = [];

    document.querySelector("#btn-agregar").addEventListener("click", () => this.mostrarFormulario(null));
    document.querySelector("#form-categoria").addEventListener("submit", (e) => {
      e.preventDefault();
      this.guardarCategoria();
    });
    document.querySelector("#btn-cancelar").addEventListener("click", () => this.ocultarFormulario());
    document.querySelector("#modal-overlay").addEventListener("click", () => this.ocultarFormulario());
    this.inputBusqueda.addEventListener("input", () => this.buscarCategoria(this.inputBusqueda.value));
    this.adapter.tbody.addEventListener("click", (e) => this.onClickTabla(e));

    this.cargarCategoria();
  }

  async cargarCategoria() {
    try {
      this.categoriasCompletas = await this.gateway.listarCategoria();
      this.adapter.setCategorias(this.categoriasCompletas);
    } catch (err) {
      this.mostrarMensaje(err.message, "error");
    }
  }

  buscarCategoria(texto) {
    const filtradas = this.categoriasCompletas.filter((c) =>
      c.nombre.toLowerCase().includes(texto.toLowerCase())
    );
    this.adapter.setCategorias(filtradas);
  }

  // Trae el dato fresco del servidor antes de editar, en vez de reusar
  // el objeto ya cargado en memoria (evita editar sobre datos desactualizados).
  async obtenerCategoria(codigo) {
    try {
      return await this.gateway.obtenerCategoria(codigo);
    } catch (err) {
      this.mostrarMensaje(err.message, "error");
      return null;
    }
  }

  mostrarFormulario(categoria) {
    this.seleccionada = categoria;
    this.inputNombre.value = categoria ? categoria.nombre : "";
    document.querySelector("#titulo-form").textContent = categoria ? "Editar categoría" : "Agregar categoría";
    document.querySelector("#modal-overlay").classList.remove("oculto");
    document.querySelector("#modal-categoria").classList.remove("oculto");
    this.inputNombre.focus();
  }

  ocultarFormulario() {
    document.querySelector("#modal-overlay").classList.add("oculto");
    document.querySelector("#modal-categoria").classList.add("oculto");
    this.seleccionada = null;
  }

  async guardarCategoria() {
    const nombre = this.inputNombre.value.trim();
    try {
      if (this.seleccionada) {
        await this.gateway.actualizarCategoria(this.seleccionada.codigo, nombre);
        this.mostrarMensaje("Categoría actualizada correctamente", "exito");
      } else {
        await this.gateway.crearCategoria(nombre);
        this.mostrarMensaje("Categoría registrada correctamente", "exito");
      }
      this.ocultarFormulario();
      this.cargarCategoria();
    } catch (err) {
      this.mostrarMensaje(err.message, "error");
    }
  }

  async eliminarCategoria(codigo, nombre) {
    const confirmar = window.confirm(`¿Eliminar la categoría "${nombre}"? Esta acción no se puede deshacer.`);
    if (!confirmar) return; // excepcion: el administrador cancela la confirmacion
    try {
      await this.gateway.eliminarCategoria(codigo);
      this.mostrarMensaje("Categoría eliminada correctamente", "exito");
      this.cargarCategoria();
    } catch (err) {
      this.mostrarMensaje(err.message, "error");
    }
  }

  async onClickTabla(e) {
    const id = e.target.dataset.id;
    if (!id) return;
    if (e.target.classList.contains("btn-editar")) {
      const categoria = await this.obtenerCategoria(id);
      if (categoria) this.mostrarFormulario(categoria);
    } else if (e.target.classList.contains("btn-eliminar")) {
      const categoria = this.categoriasCompletas.find((c) => c.codigo == id);
      this.eliminarCategoria(id, categoria ? categoria.nombre : "");
    }
  }

  mostrarMensaje(texto, tipo) {
    const toast = document.querySelector("#toast");
    toast.textContent = texto;
    toast.className = `toast ${tipo}`;
    toast.classList.remove("oculto");
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => toast.classList.add("oculto"), 2500);
  }
}

document.addEventListener("DOMContentLoaded", () => new CategoriaControladorUI());