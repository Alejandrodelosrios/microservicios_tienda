document.addEventListener("DOMContentLoaded", () => {
  const pagina = window.location.pathname.split("/").pop();
  document.querySelectorAll(".nav-link").forEach((link) => {
    if (link.getAttribute("href") === pagina) {
      link.classList.add("activo");
    }
  });
});
