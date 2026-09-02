class ApiGatewayClient {
  constructor(baseUrl = window.APP_CONFIG?.gatewayBaseUrl || "http://localhost:8080") {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  // ========== Categorias ==========

  async listarCategoria() {
    return this._request(`${this.baseUrl}/categorias`, { method: "GET" });
  }

  async obtenerCategoria(codigo) {
    return this._request(`${this.baseUrl}/categorias/${codigo}`, { method: "GET" });
  }

  async crearCategoria(nombre) {
    return this._request(`${this.baseUrl}/categorias`, {
      method: "POST",
      body: JSON.stringify({ nombre }),
    });
  }

  async actualizarCategoria(codigo, nombre) {
    return this._request(`${this.baseUrl}/categorias/${codigo}`, {
      method: "PUT",
      body: JSON.stringify({ nombre }),
    });
  }

  async eliminarCategoria(codigo) {
    return this._request(`${this.baseUrl}/categorias/${codigo}`, { method: "DELETE" });
  }

  // ========== Productos ==========

  async listarProductos() {
    return this._request(`${this.baseUrl}/productos`, { method: "GET" });
  }

  async obtenerProducto(codigo) {
    return this._request(`${this.baseUrl}/productos/${codigo}`, { method: "GET" });
  }

  async crearProducto(datos) {
    return this._request(`${this.baseUrl}/productos`, {
      method: "POST",
      body: JSON.stringify(datos),
    });
  }

  async actualizarProducto(codigo, datos) {
    return this._request(`${this.baseUrl}/productos/${codigo}`, {
      method: "PUT",
      body: JSON.stringify(datos),
    });
  }

  async eliminarProducto(codigo) {
    return this._request(`${this.baseUrl}/productos/${codigo}`, { method: "DELETE" });
  }

  // Solo usado por la vista de Productos para llenar el <select> de categoria.
  async listarCategorias() {
    return this.listarCategoria();
  }

  // ========== Interno ==========

  async _request(url, options = {}) {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });

    if (!response.ok) {
      let mensaje = `Error HTTP ${response.status}`;
      try {
        const error = await response.json();
        mensaje = error.message || error.error || mensaje;
      } catch (_) {}
      throw new Error(mensaje);
    }

    if (response.status === 204) {
      return null;
    }

    const texto = await response.text();
    return texto ? JSON.parse(texto) : null;
  }
}
