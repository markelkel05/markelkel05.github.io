document.addEventListener('DOMContentLoaded', () => {
    // Efecto de cambio de fondo del header al hacer scroll
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.style.backgroundColor = 'rgba(4, 13, 29, 0.95)'; // Más oscuro al bajar
                header.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.5)';
            } else {
                header.style.backgroundColor = 'rgba(10, 25, 47, 0.9)'; // Original
                header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.3)';
            }
        });
    }

    // Scroll suave para los enlaces de navegación
    document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Calcula la posición para tener en cuenta el header fijo
                const headerOffset = header ? header.offsetHeight : 0;
                const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                const offsetPosition = elementPosition - headerOffset - 20; // -20px extra para un pequeño margen

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});