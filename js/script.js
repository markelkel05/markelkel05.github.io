document.addEventListener('DOMContentLoaded', () => {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) { // Adjust scroll threshold as needed
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Initial hero text fade-in
    const heroElements = document.querySelectorAll('.hero .fade-in');
    heroElements.forEach(el => {
        el.classList.add('show');
    });

    // Scroll Reveal Animation
    const scrollRevealElements = document.querySelectorAll('.scroll-reveal');

    const observerOptions = {
        root: null, // Use the viewport as the root
        rootMargin: '0px',
        threshold: 0.2 // Trigger when 20% of the item is visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Stop observing once it's visible if it only animates once
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    scrollRevealElements.forEach(el => {
        observer.observe(el);
    });
});