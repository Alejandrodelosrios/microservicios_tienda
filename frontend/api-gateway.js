class ApiGateway {
  constructor(baseUrl = "http://localhost:8085") {
    this.baseUrl = baseUrl;
  }

  async listarCategoria() {
    const res = await fetch(`${this.baseUrl}/categorias`);
    if (!res.ok) throw new Error("No se pudieron obtener las categorias.");
    return res.json();
  }

  async obtenerCategoria(codigo) {
    const res = await fetch(`${this.baseUrl}/categorias/${codigo}`);
    if (!res.ok) throw new Error("No se pudo obtener la categoria.");
    return res.json();
  }

  async crearCategoria(nombre) {
    const res = await fetch(`${this.baseUrl}/categorias`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "No se pudo crear la categoria.");
    return data;
  }

  async actualizarCategoria(codigo, nombre) {
    const res = await fetch(`${this.baseUrl}/categorias/${codigo}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "No se pudo actualizar la categoria.");
    return data;
  }

  async eliminarCategoria(codigo) {
    const res = await fetch(`${this.baseUrl}/categorias/${codigo}`, { method: "DELETE" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "No se pudo eliminar la categoria.");
    return data;
  }
}