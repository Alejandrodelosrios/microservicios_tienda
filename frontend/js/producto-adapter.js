class ProductAdapter {

  constructor() {
    this.products = [];
    this.categorias = [];
  }

  setProducts(products) {
    this.products = products.map(producto =>
      ProductoDTO.fromJSON(producto)
    );
  }

  setCategorias(categorias) {
    this.categorias = categorias;
  }

  renderFila(prod) {

    const categoria =
      this.obtenerNombreCategoria(prod.categoria_codigo);

    return `
      <div class="card" data-codigo="${prod.codigo}">

        <div class="card-top">

          <div class="thumb">▣</div>

          <div class="info">

            <div class="p-name"
                 title="${this.escapeHtml(prod.nombre)}">
              ${this.escapeHtml(prod.nombre)}
            </div>

            <div class="p-meta">

              <span class="p-price">
                $${Number(prod.precio).toFixed(2)}
              </span>

              <span class="p-cat">
                ${this.escapeHtml(categoria)}
              </span>

            </div>

          </div>

        </div>

        <div class="card-actions">

          <button
            class="icon-btn edit"
            data-action="edit"
            data-codigo="${prod.codigo}">
            ✎ Editar
          </button>

          <button
            class="icon-btn del"
            data-action="delete"
            data-codigo="${prod.codigo}">
            🗑 Eliminar
          </button>

        </div>

      </div>
    `;
  }

  renderLista(query = "") {

    const termino =
      query.trim().toLowerCase();

    const productosFiltrados =
      this.products.filter(producto => {

        const categoria =
          this.obtenerNombreCategoria(
            producto.categoria_codigo
          );

        return (
          producto.nombre
            .toLowerCase()
            .includes(termino) ||

          categoria
            .toLowerCase()
            .includes(termino)
        );
      });

    document.getElementById("countTag").textContent =
      `${this.products.length} producto` +
      `${this.products.length === 1 ? "" : "s"}`;

    const grid =
      document.getElementById("grid");

    if (productosFiltrados.length === 0) {

      grid.innerHTML = `
        <div class="empty">
          No se encontraron productos.
        </div>
      `;

      return;
    }

    grid.innerHTML =
      productosFiltrados
        .map(producto =>
          this.renderFila(producto)
        )
        .join("");
  }

  obtenerNombreCategoria(categoria_codigo) {

    const categoria =
      this.categorias.find(c => {

        /*
         * MS-Categoria devuelve:
         *
         * {
         *   "codigo": 1,
         *   "nombre": "Bebidas"
         * }
         *
         * Por eso comparamos codigo
         * con categoria_codigo del producto.
         */

        return Number(c.codigo) ===
               Number(categoria_codigo);
      });

    if (!categoria) {
      return "Sin categoría";
    }

    return categoria.nombre;
  }

  escapeHtml(valor) {

    return String(valor)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
}
