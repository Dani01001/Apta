document.addEventListener("DOMContentLoaded", () => {
    // === Activar botones comentados del HTML ===
    const htmlContent = document.body.innerHTML;

    const btnReservarMatch = htmlContent.match(/<!--\s*<button[^>]*class="btn-reservar"[^>]*>.*?<\/button>\s*-->/);
    const btnReservarFloatMatch = htmlContent.match(/<!--\s*<div[^>]*class="btn-reserva-float"[^>]*>.*?<\/div>\s*-->/);

    let btnReservar, btnReservarFloat;

    if (btnReservarMatch) {
        const temp = document.createElement('div');
        temp.innerHTML = btnReservarMatch[0].replace(/<!--|-->/g, '');
        btnReservar = temp.firstElementChild;
        document.body.appendChild(btnReservar);
        btnReservar.addEventListener('click', abrirReserva);
    }

    if (btnReservarFloatMatch) {
        const temp = document.createElement('div');
        temp.innerHTML = btnReservarFloatMatch[0].replace(/<!--|-->/g, '');
        btnReservarFloat = temp.firstElementChild;
        document.body.appendChild(btnReservarFloat);
        btnReservarFloat.addEventListener('click', abrirReserva);

        // Botón flotante siempre visible
        btnReservarFloat.style.position = 'fixed';
        btnReservarFloat.style.bottom = '20px';
        btnReservarFloat.style.right = '20px';
        btnReservarFloat.style.zIndex = '999';
    }

    // === Login / Logout ===
    const registroItem = document.getElementById('registroItem');
    const loginItem = document.getElementById('loginItem');
    const userSections = document.querySelectorAll('.userSection');
    const userName = document.getElementById('userName');
    const btnLogout = document.getElementById('btnLogout');
    const btnPerfil = document.getElementById('btnPerfil');

    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    window.addEventListener("message", function(event) {
        const data = event.data;
        if (!data || data.type !== "login-success") return;
        if (data.redirect) window.location.href = data.redirect;
        else window.location.reload();
    });

    if (token && username) {
        if (registroItem) registroItem.style.display = 'none';
        if (loginItem) loginItem.style.display = 'none';
        userSections.forEach(el => el.style.display = 'flex');
        if (userName) userName.textContent = username;
    } else {
        if (registroItem) registroItem.style.display = 'inline-block';
        if (loginItem) loginItem.style.display = 'inline-block';
        userSections.forEach(el => el.style.display = 'block');
    }

    if (btnLogout) btnLogout.addEventListener('click', () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        window.location.reload();
    });
    if (btnPerfil) btnPerfil.addEventListener('click', () => window.location.href = "/usuario/");
    if (registroItem) registroItem.addEventListener('click', () => abrirVentanaEmergente('/registro/'));
    if (loginItem) loginItem.addEventListener('click', () => abrirVentanaEmergente('/login/'));

    // === Slider Menu Comida ===
    const menu = document.getElementById("menuScroll");
    const leftBtn = document.querySelector(".arrow.left");
    const rightBtn = document.querySelector(".arrow.right");

    let index = 0;
    const cardWidth = 230;
    const visibleCards = 3;
    const totalCards = menu ? menu.children.length : 0;

    if (rightBtn && menu) {
        rightBtn.addEventListener("click", () => {
            if (index < totalCards - visibleCards) {
                index++;
                menu.style.transform = `translateX(-${index * cardWidth}px)`;
            }
        });
    }
    if (leftBtn && menu) {
        leftBtn.addEventListener("click", () => {
            if (index > 0) {
                index--;
                menu.style.transform = `translateX(-${index * cardWidth}px)`;
            }
        });
    }

    // === Avatar aleatorio ===
    const avatar = document.getElementById("userAvatar");
    if (avatar) {
        const colors = ["#e63946", "#f1faee", "#a8dadc", "#457b9d", "#1d3557", "#ffbe0b", "#fb5607", "#ff006e"];
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        avatar.style.backgroundColor = randomColor;
    }

    // === Fetch API ejemplo ===
    fetch("/api/reservas/lista/")
        .then(res => {
            if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            console.log("✅ Datos recibidos desde la API:", data);
        })
        .catch(error => {
            console.error("❌ Error al conectar con la API", error);
        });
});

// === Funciones auxiliares ===
function abrirVentanaEmergente(url) {
    const ancho = 700;
    const alto = 850;
    const left = (window.innerWidth - ancho) / 2;
    const top = (window.innerHeight - alto) / 2;

    const ventana = window.open(url, "VentanaEmergente", `width=${ancho},height=${alto},top=${top},left=${left}`);
    const intervalo = setInterval(() => {
        if (ventana.closed) {
            clearInterval(intervalo);
            window.location.reload();
        }
    }, 500);
}

function abrirReserva() {
    const params = new URLSearchParams(window.location.search);
    const restauranteId = params.get('restaurante') || 1;

    const width = 700;
    const height = 700;
    const left = window.screenX + (window.outerWidth - width) / 2;
    const top = window.screenY + (window.outerHeight - height) / 2;

    window.open(
        `/reservas/pagina/?restaurante=${restauranteId}`,
        "ReservaYa",
        `popup=yes,width=${width},height=${height},left=${left},top=${top},toolbar=no,location=no,status=no,scrollbars=no,resizable=no`
    );
}
