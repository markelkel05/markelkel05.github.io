document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });

            // Close mobile menu after clicking a link
            if (window.innerWidth <= 768) {
                const navList = document.querySelector('.nav-list');
                const hamburger = document.querySelector('.hamburger');
                navList.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    });

    // Hamburger menu functionality
    const hamburger = document.querySelector('.hamburger');
    const navList = document.querySelector('.nav-list');

    hamburger.addEventListener('click', () => {
        navList.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Highlight active navigation link on scroll
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-list a');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href').substring(1) === entry.target.id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { threshold: 0.5 }); // Adjust threshold as needed

    sections.forEach(section => {
        observer.observe(section);
    });

    // Special handling for hero section if its ID is not 'hero'
    const heroSection = document.getElementById('hero');
    if (heroSection) {
        // If the hero section is at the very top, ensure 'Inicio' is active
        // This might be redundant if the observer handles it, but good for explicit initial state.
        if (window.scrollY === 0) {
            document.querySelector('a[href="#hero"]').classList.add('active');
        }
    }
});