document.addEventListener("DOMContentLoaded", function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

        // === BOTÓN VOLVER ===
    const backButton = document.getElementById("backButton");
    if (backButton) {
        backButton.addEventListener("click", () => {
            window.location.href = "/"; // Cambie a su URL home si es diferente
        });
    }

    // === Actualizar contadores ===
    function actualizarContadores() {
        const reservas = document.querySelectorAll("#tablaReservas tr");
        let hoy = 0, pendientes = 0, confirmadas = 0, canceladas = 0;
        const hoyFecha = new Date().toISOString().split('T')[0];

        reservas.forEach(tr => {
            const estadoSelect = tr.querySelector(".estadoReserva");
            if (!estadoSelect) return;

            const estado = estadoSelect.value;
            const fecha = tr.children[2].textContent.trim();

            if (fecha === hoyFecha) hoy++;
            if (estado === "Pendiente") pendientes++;
            if (estado === "Confirmada") confirmadas++;
            if (estado === "Cancelada") canceladas++;
        });

        document.getElementById("valorHoy").textContent = hoy;
        document.getElementById("valorPendientes").textContent = pendientes;
        document.getElementById("valorConfirmadas").textContent = confirmadas;
        document.getElementById("valorCanceladas").textContent = canceladas;
    }

    actualizarContadores();

    // === Modo diferido: guardar cambios después ===
    const cambiosPendientes = {};

    document.querySelectorAll(".estadoReserva").forEach(select => {
        select.addEventListener("change", function () {
            const reservaId = this.dataset.id;
            const nuevoEstado = this.value;
            cambiosPendientes[reservaId] = nuevoEstado; // Guardamos el cambio en memoria local
            this.closest("tr").classList.add("table-warning"); // Marca la fila como pendiente
            actualizarContadores();
        });
    });

    // === Botón de guardado ===
    const guardarCambiosBtn = document.getElementById("guardarCambiosBtn");
    guardarCambiosBtn.addEventListener("click", function () {
        if (Object.keys(cambiosPendientes).length === 0) {
            alert("No hay cambios pendientes.");
            return;
        }

        if (!confirm("¿Desea guardar los cambios realizados en las reservas?")) return;

        fetch("/restaurantes/gestionar/actualizar_estado_multiple/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(cambiosPendientes)
        })
        .then(resp => resp.json())
        .then(data => {
            if (data.success) {
                alert("Cambios guardados correctamente.");
                document.querySelectorAll("tr.table-warning").forEach(tr => tr.classList.remove("table-warning"));
                for (let id in cambiosPendientes) delete cambiosPendientes[id];
                actualizarContadores();
            } else {
                alert(data.error || "Error al guardar los cambios.");
            }
        })
        .catch(() => alert("Error de red al guardar los cambios."));
    });


    // === MODAL DE MESAS ===
    const mesaModal = document.getElementById("mesaModal");
    const abrirMesaModal = document.getElementById("abrirMesaModal");
    const cerrarMesaModal = document.getElementById("closeMesaModal");
    const mesaForm = document.getElementById("mesaForm");
    const mesaIdInput = document.getElementById("mesaId");
    const mesaNumberInput = document.getElementById("mesaNumber");
    const mesaCapacityInput = document.getElementById("mesaCapacity");
    const mesaLocationInput = document.getElementById("mesaLocation");
    const mesaDescriptionInput = document.getElementById("mesaDescription");
    const modalTitle = document.getElementById("modalMesaTitle");

    abrirMesaModal.addEventListener("click", () => {
        mesaForm.reset();
        mesaIdInput.value = "";
        modalTitle.textContent = "Agregar Mesa";
        mesaModal.style.display = "block";
    });

    cerrarMesaModal.addEventListener("click", () => {
        mesaModal.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target === mesaModal) mesaModal.style.display = "none";
    });

    // === GUARDAR / EDITAR MESA ===
    mesaForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const mesaId = mesaIdInput.value;
        const numero = mesaNumberInput.value;
        const capacidad = mesaCapacityInput.value;
        const ubicacion = mesaLocationInput.value;
        const descripcion = mesaDescriptionInput.value;

        const url = mesaId
            ? `/restaurantes/gestionar/editar_mesa_ajax/${mesaId}/`
            : `/restaurantes/gestionar/agregar_mesa_ajax/`;

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrftoken
            },
            body: `numero=${numero}&capacidad=${capacidad}&ubicacion=${ubicacion}&descripcion=${descripcion}`
        })
        .then(resp => resp.json())
        .then(data => {
            if (data.success) {
                alert("Mesa guardada correctamente.");
                location.reload();
            } else {
                alert(data.error || "Error al guardar la mesa.");
            }
        })
        .catch(() => alert("Error de red al guardar mesa."));
    });

    // === ELIMINAR MESA ===
    document.querySelectorAll(".eliminarMesa").forEach(btn => {
        btn.addEventListener("click", function () {
            const mesaId = this.dataset.id;
            if (!confirm("¿Seguro que desea eliminar esta mesa?")) return;

            fetch(`/restaurantes/gestionar/eliminar_mesa/${mesaId}/`, {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken }
            })
            .then(resp => resp.json())
            .then(data => {
                if (data.success) {
                    alert("Mesa eliminada correctamente.");
                    document.querySelector(`tr[data-id="${mesaId}"]`)?.remove();
                } else {
                    alert(data.error || "Error al eliminar la mesa.");
                }
            })
            .catch(() => alert("Error de red al eliminar mesa."));
        });
    });

    // === EDITAR MESA ===
    document.querySelectorAll(".editarMesaBtn").forEach(btn => {
        btn.addEventListener("click", function () {
            const fila = this.closest("tr");
            mesaIdInput.value = fila.dataset.id;
            mesaNumberInput.value = fila.children[0].textContent.trim();
            mesaCapacityInput.value = fila.children[1].textContent.trim();
            mesaLocationInput.value = fila.children[2].textContent.trim().toLowerCase();
            modalTitle.textContent = "Editar Mesa";
            mesaModal.style.display = "block";
        });
    });

});
