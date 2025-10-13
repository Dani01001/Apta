document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formReserva");
    const mensaje = document.getElementById("mensaje-reserva");

    // Autocompletar el nombre del usuario logueado
    fetch("/api/usuario/logueado/") // Debe crear esta API que devuelve {username: "NombreUsuario"}
        .then(res => res.json())
        .then(data => {
            if (data.username) {
                document.getElementById("nombre").value = data.username;
            }
        })
        .catch(err => console.error("No se pudo obtener usuario logueado", err));

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrfToken = getCookie("csrftoken");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        mensaje.innerText = "⏳ Reservando...";
        mensaje.className = "";
        
        const data = {
            restaurante_id: parseInt(document.getElementById("restaurante").value),
            nombre_cliente: document.getElementById("nombre").value,
            fecha: document.getElementById("fecha").value,
            hora: document.getElementById("hora").value,
            duracion_horas: parseFloat(document.getElementById("duracion").value),
            cantidad_personas: parseInt(document.getElementById("personas").value)
        };

        try {
            const token = localStorage.getItem("token");
            const response = await fetch("/reservas/api/crear/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                    ...(token ? { "Authorization": `Token ${token}` } : {})
                },
                credentials: "include",
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                mensaje.innerHTML = `✅ Reserva creada con éxito.<br>
                    Mesa asignada: <b>${result.mesa.numero}</b><br>
                    Código de reserva: <b>${result.codigo_reserva || "N/A"}</b><br>
                    Estado: <b>${result.estado}</b>`;
                mensaje.className = "success";
                form.reset();
                document.getElementById("nombre").value = result.nombre_cliente || "";
            } else {
                let errorMsg = "";
                if (typeof result === "object") {
                    for (let key in result) {
                        if (Array.isArray(result[key])) {
                            errorMsg += `<div>${key}: ${result[key].join(", ")}</div>`;
                        } else {
                            errorMsg += `<div>${key}: ${result[key]}</div>`;
                        }
                    }
                } else {
                    errorMsg = "❌ No se pudo crear la reserva.";
                }
                mensaje.innerHTML = errorMsg;
                mensaje.className = "error";
            }
        } catch (err) {
            mensaje.innerText = "⚠️ Error de conexión con el servidor.";
            mensaje.className = "error";
            console.error(err);
        }
    });
});
