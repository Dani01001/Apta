document.addEventListener("DOMContentLoaded", function () {
    // Actualiza los contadores del dashboard
    function actualizarContadores() {
        const reservas = document.querySelectorAll("#tablaReservas tr");
        let hoy = 0, pendientes = 0, confirmadas = 0, canceladas = 0;

        const hoyFecha = new Date().toISOString().split('T')[0];

        reservas.forEach(tr => {
            const estadoSelect = tr.querySelector(".estadoReserva");
            if (!estadoSelect) return; // evita null

            const estado = estadoSelect.value;
            const fecha = tr.children[2].textContent;

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

    // Cambiar estado de reserva vía AJAX
    document.querySelectorAll(".estadoReserva").forEach(select => {
        select.addEventListener("change", function () {
            const reservaId = this.dataset.id;
            const nuevoEstado = this.value;

            fetch(`/restaurantes/admin/restaurante/actualizar_estado/${reservaId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie('csrftoken')
                },
                body: `estado=${nuevoEstado}`
            })
            .then(resp => resp.json())
            .then(data => {
                if (data.success) {
                    actualizarContadores();
                } else {
                    alert(data.error || "Error al actualizar estado");
                }
            })
            .catch(err => alert("Error de red al actualizar estado"));
        });
    });

    // Eliminar mesa vía AJAX
    document.querySelectorAll(".eliminarMesaBtn").forEach(btn => {
        btn.addEventListener("click", function () {
            const mesaId = this.dataset.id;
            if (!confirm("¿Seguro que desea eliminar esta mesa?")) return;

            fetch(`/restaurantes/admin/restaurante/eliminar_mesa/${mesaId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                }
            })
            .then(resp => resp.json())
            .then(data => {
                if (data.success) {
                    const fila = document.querySelector(`#tablaMesas tr[data-id='${mesaId}']`);
                    if (fila) fila.remove();
                } else {
                    alert(data.error || "Error al eliminar mesa");
                }
            });
        });
    });

    // Función para obtener cookie CSRF (necesaria para POST en Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
