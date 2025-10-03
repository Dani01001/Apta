document.addEventListener("DOMContentLoaded", () => {
  const abrir = (id) => document.getElementById(id).style.display = "block";
  const cerrar = (id) => document.getElementById(id).style.display = "none";

  document.getElementById("btnLogin").addEventListener("click", () => abrir("modalLogin"));
  document.getElementById("btnRegistro").addEventListener("click", () => abrir("modalRegistro"));

  document.querySelectorAll(".cerrar").forEach(btn => {
    btn.addEventListener("click", () => cerrar(btn.dataset.close));
  });

  // cerrar al hacer clic fuera
  window.addEventListener("click", (e) => {
    document.querySelectorAll(".modal").forEach(modal => {
      if (e.target === modal) modal.style.display = "none";
    });
  });
});
