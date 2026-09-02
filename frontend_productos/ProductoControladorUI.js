class ProductoControladorUI {

  constructor() {

    this.inputNombre =
      document.getElementById("fName");

    this.inputPrecio =
      document.getElementById("fPrice");

    this.selectCategoria =
      document.getElementById("fCategory");

    this.seleccionado = null;

    // API Gateway que comunica con:
    // MS-Producto    -> puerto 8086
    // MS-Categoria   -> puerto 8085
    this.apiGateway =
      new ApiGatewayProducto();

    // Adapter encargado de pintar los productos
    this.adapter =
      new ProductAdapter();

    this.overlay =
      document.getElementById("overlay");

    this.grid =
      document.getElementById("grid");

    this.searchInput =
      document.getElementById("searchInput");

    this.editandoCodigo = null;

    this.inicializarEventos();
    this.inicializar();
  }

  /**
   * Inicializa la información necesaria
   * para mostrar la vista.
   */
  async inicializar() {

    await this.cargarCategoria();

    await this.cargarProducto();
  }

  /**
   * Eventos de la interfaz.
   */
  inicializarEventos() {

    // Nuevo producto
    document.getElementById("openAdd")
      .addEventListener("click", () => {

        this.abrirFormulario();

      });


    // Cerrar modal
    document.getElementById("closeModal")
      .addEventListener("click", () => {

        this.cerrarFormulario();

      });


    // Cancelar
    document.getElementById("cancelBtn")
      .addEventListener("click", () => {

        this.cerrarFormulario();

      });


    // Guardar
    document.getElementById("saveBtn")
      .addEventListener("click", () => {

        this.guardarProducto();

      });


    // Buscar productos
    this.searchInput.addEventListener(
      "input",
      () => {

        this.buscarProducto(
          this.searchInput.value
        );

      }
    );


    // Eventos de editar y eliminar
    this.grid.addEventListener(
      "click",
      async event => {

        const boton =
          event.target.closest(
            "[data-action]"
          );

        if (!boton) {
          return;
        }

        const codigo =
          Number(boton.dataset.codigo);


        // Editar
        if (
          boton.dataset.action ===
          "edit"
        ) {

          // Trae el dato fresco del servidor antes de editar,
          // en vez de reusar el objeto ya cargado en memoria
          // (evita editar sobre datos desactualizados).
          const producto =
            await this.obtenerProducto(
              codigo
            );

          if (producto) {

            this.abrirFormulario(
              producto
            );

          }
        }


        // Eliminar
        if (
          boton.dataset.action ===
          "delete"
        ) {

          this.eliminarProducto(codigo);

        }

      }
    );


    // Cerrar modal haciendo click fuera
    this.overlay.addEventListener(
      "click",
      event => {

        if (
          event.target ===
          this.overlay
        ) {

          this.cerrarFormulario();

        }

      }
    );
  }


  /**
   * Obtiene los productos desde
   * MS-Producto.
   *
   * GET http://localhost:8086/productos
   */
  async cargarProducto() {

    try {

      const respuesta =
        await this.apiGateway
          .listarProductos();


      const productos =
        Array.isArray(respuesta)
          ? respuesta
          : respuesta?.data ??
            respuesta?.productos ??
            [];


      /*
       * El Adapter convierte cada
       * producto en ProductoDTO.
       */
      this.adapter.setProducts(
        productos
      );


      /*
       * Después el Adapter pinta
       * los productos en el HTML.
       */
      this.adapter.renderLista(
        this.searchInput.value
      );

    } catch (error) {

      console.error(error);

      this.adapter.setProducts([]);

      this.adapter.renderLista();

      this.mostrarMensaje(
        "No se pudieron cargar los productos: " +
        error.message,
        "error"
      );
    }
  }


  /**
   * Obtiene un producto puntual desde
   * MS-Producto.
   *
   * GET http://localhost:8086/productos/{codigo}
   */
  async obtenerProducto(codigo) {

    try {

      return await this.apiGateway
        .obtenerProducto(codigo);

    } catch (error) {

      console.error(error);

      this.mostrarMensaje(
        "No se pudo obtener el producto: " +
        error.message,
        "error"
      );

      return null;
    }
  }


  /**
   * Filtra la lista de productos ya
   * cargada en memoria por nombre o
   * categoría.
   */
  buscarProducto(texto) {

    this.adapter.renderLista(texto);
  }


  /**
   * Obtiene las categorías desde
   * MS-Categoria.
   *
   * GET http://localhost:8085/categorias
   */
  async cargarCategoria() {

    try {

      const respuesta =
        await this.apiGateway
          .listarCategorias();


      const categorias =
        Array.isArray(respuesta)
          ? respuesta
          : respuesta?.data ??
            respuesta?.categorias ??
            [];


      /*
       * MS-Categoria devuelve:
       *
       * {
       *   "codigo": 1,
       *   "nombre": "Bebidas"
       * }
       */
      this.adapter.setCategorias(
        categorias
      );


      this.pintarCategorias();

    } catch (error) {

      console.warn(
        "No se pudieron cargar categorías:",
        error
      );


      /*
       * Datos de respaldo.
       *
       * Se utilizan únicamente si
       * MS-Categoria no responde.
       *
       * IMPORTANTE:
       * ahora utilizamos "codigo"
       * porque esa es la propiedad
       * que devuelve tu backend.
       */
      const categorias = [

        {
          codigo: 1,
          nombre: "Bebidas"
        },

        {
          codigo: 2,
          nombre: "Alimentos"
        },

        {
          codigo: 3,
          nombre: "Limpieza"
        },

        {
          codigo: 4,
          nombre: "Electrónica"
        },

        {
          codigo: 5,
          nombre: "Otros"
        }

      ];


      this.adapter.setCategorias(
        categorias
      );

      this.pintarCategorias();
    }
  }


  /**
   * Pinta las categorías dentro
   * del <select>.
   *
   * MS-Categoria:
   *
   * codigo -> identificador
   * nombre -> texto visible
   */
  pintarCategorias() {

    this.selectCategoria.innerHTML =

      this.adapter.categorias
        .map(categoria => `

          <option
            value="${categoria.codigo}"
          >
            ${this.adapter.escapeHtml(
              categoria.nombre
            )}
          </option>

        `)
        .join("");
  }


  /**
   * Crea o actualiza un producto.
   */
  async guardarProducto() {

    const nombre =
      this.inputNombre.value.trim();


    const precio =
      Number.parseFloat(
        this.inputPrecio.value
      );


    /*
     * El select contiene:
     *
     * value = codigo de categoria
     *
     * Por eso obtenemos el valor
     * como categoria_codigo.
     */
    const categoria_codigo =
      Number(
        this.selectCategoria.value
      );


    // Validar nombre
    if (!nombre) {

      this.mostrarMensaje(
        "El nombre es obligatorio.",
        "error"
      );

      return;
    }


    // Validar precio
    if (
      Number.isNaN(precio) ||
      precio < 0
    ) {

      this.mostrarMensaje(
        "El precio no es válido.",
        "error"
      );

      return;
    }


    /*
     * Crear ProductoDTO.
     *
     * El DTO representa el objeto
     * que se enviará al MS-Producto.
     */
    const dto =
      new ProductoDTO(
        this.editandoCodigo,
        nombre,
        precio,
        categoria_codigo
      );


    try {

      /*
       * ACTUALIZAR
       */
      if (
        this.editandoCodigo !== null
      ) {

        await this.apiGateway
          .actualizarProducto(
            this.editandoCodigo,
            dto.toJSON()
          );

      }

      /*
       * CREAR
       */
      else {

        await this.apiGateway
          .crearProducto(
            dto.toJSON()
          );
      }


      const eraEdicion =
        this.editandoCodigo !== null;


      this.cerrarFormulario();


      /*
       * Volvemos a consultar
       * los productos para actualizar
       * la vista.
       */
      await this.cargarProducto();


      this.mostrarMensaje(

        eraEdicion
          ? "Producto actualizado correctamente."
          : "Producto creado correctamente.",

        "success"
      );

    } catch (error) {

      console.error(error);

      this.mostrarMensaje(
        "No se pudo guardar: " +
        error.message,
        "error"
      );
    }
  }


  /**
   * Elimina un producto.
   *
  * DELETE http://localhost:8086/productos/{codigo}
   */
  async eliminarProducto(codigo) {

    const producto =
      this.adapter.products.find(
        p => Number(p.codigo) === codigo
      );


    if (!producto) {
      return;
    }


    const confirmar =
      confirm(
        `¿Deseas eliminar "${producto.nombre}"?`
      );


    if (!confirmar) {
      return;
    }


    try {

      await this.apiGateway
        .eliminarProducto(codigo);


      /*
       * Recargar productos después
       * de eliminar.
       */
      await this.cargarProducto();


      this.mostrarMensaje(
        "Producto eliminado correctamente.",
        "success"
      );

    } catch (error) {

      console.error(error);

      this.mostrarMensaje(
        "No se pudo eliminar: " +
        error.message,
        "error"
      );
    }
  }


  /**
   * Abre el formulario.
   *
   * Si producto == null:
   *     Crear producto
   *
   * Si producto != null:
   *     Editar producto
   */
  abrirFormulario(
    producto = null
  ) {

    this.seleccionado =
      producto;


    this.editandoCodigo =
      producto
        ? Number(producto.codigo)
        : null;


    /*
     * Título del modal.
     */
    document.getElementById(
      "modalEyebrow"
    ).textContent =

      producto
        ? "Actualizar datos"
        : "Inventario";


    document.getElementById(
      "modalTitle"
    ).textContent =

      producto
        ? "Actualizar producto"
        : "Registrar producto";


    /*
     * Cargar nombre.
     */
    this.inputNombre.value =

      producto
        ? producto.nombre
        : "";


    /*
     * Cargar precio.
     */
    this.inputPrecio.value =

      producto
        ? producto.precio
        : "";


    /*
     * Seleccionar categoría.
     *
     * producto.categoria_codigo corresponde
     * al categoria.codigo del MS-Categoria.
     */
    this.selectCategoria.value =

      producto
        ? producto.categoria_codigo
        : this.selectCategoria
            .options[0]?.value ?? "";


    /*
     * Mostrar modal.
     */
    this.overlay.classList.add(
      "active"
    );


    this.inputNombre.focus();
  }


  /**
   * Cierra y limpia el formulario.
   */
  cerrarFormulario() {

    this.overlay.classList.remove(
      "active"
    );


    this.editandoCodigo = null;

    this.seleccionado = null;


    this.inputNombre.value = "";

    this.inputPrecio.value = "";
  }


  /**
   * Mostrar mensaje.
   *
   * Actualmente utiliza alert().
   */
  mostrarMensaje(
    msg,
    tipo = "info"
  ) {

    alert(msg);
  }
}


/*
 * Iniciar controlador cuando
 * el HTML termine de cargar.
 */
document.addEventListener(
  "DOMContentLoaded",
  () => {

    window.productoControladorUI =
      new ProductoControladorUI();

  }
);