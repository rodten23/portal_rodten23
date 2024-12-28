/* Abre e fecha menu lateral em modo mobile. */

const menuMobile = document.querySelector('.menu-mobile');
const body = document.querySelector('body');

menuMobile.addEventListener('click', () => {
    menuMobile.classList.contains('bi-list')
    ? menuMobile.classList.replace('bi-list', 'bi-x')
    : menuMobile.classList.replace('bi-x', 'bi-list');
    body.classList.toggle('menu-nav-active');
});


/* Fecha o menu quando clicar em algum item e mudo o ícone para list. */

const navItem = document.querySelectorAll('.nav-item')

navItem.forEach(item => {
    item.addEventListener("click", () => {
        if (body.classList.contains("menu-nav-active")) {
            body.classList.remove("menu-nav-active")
            menuMobile.classList.replace("bi-x", "bi-list");
        }
    })
})

// Animar todos os itens na tela que tiverem o atributo data-anime

const item = document.querySelectorAll("[data-anime]");

const animeScroll = () => {
    const windowTop = window.scrollY + window.innerHeight * 0.85;

    item.forEach((element) => {
        if (windowTop > element.offsetTop) {
            element.classList.add("animate");
        } else {
            element.classList.remove("animate");
        }
    });
}

animeScroll();

window.addEventListener("scroll", ()=> {
    animeScroll();
})

// Ativar carregamento no botão de enviar formulário

const btnEnviar = document.querySelector('#btn-enviar')
const btnEnviando = document.querySelector('#btn-enviando')

btnEnviar.addEventListener("click", () => {
    btnEnviando.style.display = "block";
    btnEnviar.style.display = "none"
})

// Tirar mensagem (alerta) de sucesso depois de 5 segundos (5000 milisegundos)

setTimeout( () => {
    document.querySelector('#alerta').style.display = 'none';

}, 5000)
