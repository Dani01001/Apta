document.addEventListener("DOMContentLoaded", () => {
    const userSections = document.querySelectorAll('.userSection');
    const registroItem = document.getElementById('registroItem');
    const loginItem = document.getElementById('loginItem');
    const userName = document.getElementById('userName');
    const btnLogout = document.getElementById('btnLogout');
    const btnPerfil = document.getElementById('btnPerfil');

    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

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

    if (btnLogout) {
        btnLogout.addEventListener('click', () => {
            localStorage.removeItem("token");
            localStorage.removeItem("username");
            window.location.reload();
        });
    }

    if (btnPerfil) {
        btnPerfil.addEventListener('click', () => {
            window.location.href = "/usuario/";
        });
    }

    if (registroItem) {
        registroItem.addEventListener('click', () => abrirVentanaEmergente('/registro/'));
    }

    if (loginItem) {
        loginItem.addEventListener('click', () => abrirVentanaEmergente('/login/'));
    }
});

function abrirVentanaEmergente(url) {
    const ancho = 700;
    const alto = 850;
    const left = (window.innerWidth - ancho) / 2;
    const top = (window.innerHeight - alto) / 2;

    const ventana = window.open(
        url,
        "VentanaEmergente",
        `width=${ancho},height=${alto},top=${top},left=${left}`
    );

    const intervalo = setInterval(() => {
        if (ventana.closed) {
            clearInterval(intervalo);
            window.location.reload();
        }
    }, 500);
}

// === SLIDER ===
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
