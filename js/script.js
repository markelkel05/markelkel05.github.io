// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Función simple para un efecto de scroll suave en los enlaces de ancla
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - (document.querySelector('.header').offsetHeight || 80), // Ajusta para el header fijo
                    behavior: 'smooth'
                });
            }
        });
    });

    // Opcional: Cambiar el estilo del header al hacer scroll
    const header = document.querySelector('.header');
    const heroSection = document.getElementById('hero');

    const changeHeaderStyle = () => {
        if (heroSection) {
            const heroHeight = heroSection.offsetHeight;
            if (window.scrollY > heroHeight - 100) { // Cambia el color del header cuando se sale de la sección hero
                header.style.backgroundColor = 'var(--primary-blue)';
                header.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.4)';
            } else {
                header.style.backgroundColor = 'rgba(10, 28, 44, 0.9)';
                header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.2)';
            }
        }
    };

    window.addEventListener('scroll', changeHeaderStyle);
    changeHeaderStyle(); // Ejecutar al cargar para establecer el estado inicial

    // Aquí no se necesita JavaScript para el efecto parallax básico
    // porque background-attachment: fixed ya lo maneja. 
    // JS sería necesario para efectos parallax más complejos (ej. diferentes velocidades de elementos).
    // Pero para este requisito, el CSS es suficiente.
});
