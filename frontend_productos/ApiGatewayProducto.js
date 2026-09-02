class ApiGatewayProducto {

  constructor(
    productoBaseUrl = "http://localhost:8086",
    categoriaBaseUrl = "http://localhost:8085"
  ) {
    this.productoBaseUrl = productoBaseUrl.replace(/\/$/, "");
    this.categoriaBaseUrl = categoriaBaseUrl.replace(/\/$/, "");
  }

  // =========================
  // MICRO SERVICIO PRODUCTO
  // =========================

  async crearProducto(datos) {
    return this._request(
      `${this.productoBaseUrl}/productos`,
      {
        method: "POST",
        body: JSON.stringify(datos)
      }
    );
  }

  async actualizarProducto(codigo, datos) {
    return this._request(
      `${this.productoBaseUrl}/productos/${codigo}`,
      {
        method: "PUT",
        body: JSON.stringify(datos)
      }
    );
  }

  async eliminarProducto(codigo) {
    return this._request(
      `${this.productoBaseUrl}/productos/${codigo}`,
      {
        method: "DELETE"
      }
    );
  }

  async listarProductos() {
    return this._request(
      `${this.productoBaseUrl}/productos`,
      {
        method: "GET"
      }
    );
  }

  async obtenerProducto(codigo) {
    return this._request(
      `${this.productoBaseUrl}/productos/${codigo}`,
      {
        method: "GET"
      }
    );
  }

  // =========================
  // MICRO SERVICIO CATEGORIA
  // =========================

  async listarCategorias() {
    return this._request(
      `${this.categoriaBaseUrl}/categorias`,
      {
        method: "GET"
      }
    );
  }

  async _request(url, options = {}) {

    const response = await fetch(
      url,
      {
        ...options,

        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {})
        }
      }
    );

    if (!response.ok) {

      let mensaje =
        `Error HTTP ${response.status}`;

      try {

        const error =
          await response.json();

        mensaje =
          error.message ||
          error.error ||
          mensaje;

      } catch (_) {}

      throw new Error(mensaje);
    }

    if (response.status === 204) {
      return null;
    }

    const texto =
      await response.text();

    return texto
      ? JSON.parse(texto)
      : null;
  }
}