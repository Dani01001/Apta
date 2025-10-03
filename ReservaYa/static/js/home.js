document.addEventListener("DOMContentLoaded", () => {
//     const userInfo = document.getElementById('userInfo');
//     const btnReservar = document.querySelector(".btn-reservar");
//     const btnReservarFloat = document.querySelector(".btn-reserva-float");
//     const registroItem = document.getElementById('registroItem');
//     const loginItem = document.getElementById('loginItem');
//     const userName = document.getElementById('userName');
//     const btnLogout = document.getElementById('btnLogout');
//     const btnPerfil = document.getElementById('btnPerfil');
//     const token = localStorage.getItem("token");
//     const username = localStorage.getItem("username");
//     const userSections = document.querySelectorAll('.userSection');
//     window.addEventListener("message", function(event) {
//         const data = event.data;
//         if (!data || data.type !== "login-success") return;

//         console.log("Mensaje recibido:", data);
//         if (data.redirect) {
//             window.location.href = data.redirect;
//         } else {
//             window.location.reload();
//         }
//     });
//     if (token && username) {
//         if (registroItem) registroItem.style.display = 'none';
//         if (loginItem) loginItem.style.display = 'none';

//         userSections.forEach(el => el.style.display = 'flex'); 
//         if (userName) userName.textContent = username;
//     } else {
//         if (registroItem) registroItem.style.display = 'inline-block';
//         if (loginItem) loginItem.style.display = 'inline-block';
//         userSections.forEach(el => el.style.display = 'block');
//     }

//     if (btnLogout) {
//         btnLogout.addEventListener('click', () => {
//             localStorage.removeItem("token");
//             localStorage.removeItem("username");
//             window.location.reload();
//         });
//     }
//     if (btnPerfil) {
//         btnPerfil.addEventListener('click', () => {
//             window.location.href = "/usuario/";
//         });
//     }
//     if (registroItem) {
//         registroItem.addEventListener('click', () => abrirVentanaEmergente('/registro/'));
//     }
//     if (loginItem) {
//         loginItem.addEventListener('click', () => abrirVentanaEmergente('/login/'));
//     }

//     if (btnReservar) {
//         btnReservar.addEventListener("click", () => abrirReserva());
//     }
//     if (btnReservarFloat) {
//         btnReservarFloat.addEventListener("click", () => abrirReserva());
//     }
});

function abrirVentanaEmergente(url) {
    const ancho = 700;
    const alto = 850;
    const left = (window.innerWidth - ancho) / 2;
    const top = (window.innerHeight - alto) / 2;

    // Abrir la ventana
    const ventana = window.open(
        url,
        "VentanaEmergente",
        `width=${ancho},height=${alto},top=${top},left=${left}`
    );

    // Comprobar si ventana se cerró y refrescar la principal
    const intervalo = setInterval(() => {
        if (ventana.closed) {
            clearInterval(intervalo);
            window.location.reload(); // fuerza recarga de la principal
        }
    }, 500);
}


// function abrirReserva() {
//     const params = new URLSearchParams(window.location.search);
//     const restauranteId = params.get('restaurante') || 1;

//     const width = 700;
//     const height = 700;
//     const left = window.screenX + (window.outerWidth - width) / 2;
//     const top = window.screenY + (window.outerHeight - height) / 2;

//     window.open(
//         `/reservas/pagina/?restaurante=${restauranteId}`,
//         "ReservaYa",
//         `popup=yes,width=${width},height=${height},left=${left},top=${top},
//         toolbar=no,location=no,status=no,scrollbars=no,resizable=no`
//     );
// }

// ==== API FETCH =====
// fetch("/api/reservas/lista/")
//     .then(res => {
//         if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
//         return res.json();
//     })
//     .then(data => {
//         console.log("✅ Datos recibidos desde la API:", data);
//     })
//     .catch(error => {
//         console.error("❌ Error al conectar con la API", error);
//     });

// ==== SLIDER =====
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

