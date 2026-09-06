/**
 * ProductoDTO
 *
 * Objeto de transferencia de datos utilizado por la interfaz
 * para representar un producto.
 */
class ProductoDTO {
  constructor(codigo, nombre, precio, categoria_codigo) {
    this.codigo = codigo;
    this.nombre = nombre;
    this.precio = Number(precio);
    this.categoria_codigo = Number(categoria_codigo);
  }

  /**
   * Convierte una respuesta de API a ProductoDTO.
   */
  static fromJSON(data) {
    return new ProductoDTO(
      data.codigo,
      data.nombre ?? data.name,
      data.precio ?? data.price,
      data.categoria_codigo
    );
  }

  /**
   * Convierte el DTO al objeto que se enviará al backend.
   */
  toJSON() {
    return {
      codigo: this.codigo,
      nombre: this.nombre,
      precio: this.precio,
      categoria_codigo: this.categoria_codigo
    };
  }
}
