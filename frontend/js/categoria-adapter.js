class CategoriaAdapter {
  constructor(tbody) {
    this.tbody = tbody;
    this.categorias = [];
  }

  setCategorias(categorias) {
    this.categorias = categorias;
    this.renderLista();
  }

  renderFila(categoria) {
    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td>${categoria.nombre}</td>
      <td class="acciones">
        <button class="btn-icono btn-editar" data-id="${categoria.codigo}" title="Editar">✎</button>
        <button class="btn-icono btn-eliminar" data-id="${categoria.codigo}" title="Eliminar">🗑</button>
      </td>`;
    return fila;
  }

  renderLista() {
    this.tbody.innerHTML = "";
    if (this.categorias.length === 0) {
      this.tbody.innerHTML = `<tr><td colspan="2" class="vacio">No se encontraron categorias</td></tr>`;
      return;
    }
    this.categorias.forEach((cat) => this.tbody.appendChild(this.renderFila(cat)));
  }
}
