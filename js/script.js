document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });

            // Close mobile menu if open
            const navMenu = document.getElementById('navMenu');
            const hamburger = document.getElementById('hamburger');
            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    });

    // Mobile navigation toggle
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');

    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Add 'active' class to nav links on scroll
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-menu a');
    const headerHeight = document.querySelector('.header').offsetHeight; // Get header height dynamically

    const observerOptions = {
        root: null,
        rootMargin: `-${headerHeight}px 0px 0px 0px`, // Adjust for fixed header height
        threshold: 0.1 // Trigger when 10% of the section is visible (below the header)
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.intersectionRatio >= 0.1) { 
                // Remove active class from all links
                navLinks.forEach(link => link.classList.remove('active'));

                // Add active class to the link corresponding to the intersecting section
                const targetId = entry.target.id;
                const activeLink = document.querySelector(`.nav-menu a[href="#${targetId}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });

    // Ensure 'Inicio' is active on page load or when scrolled to the top
    const initialActiveLink = document.querySelector('.nav-menu a[href="#hero"]');
    if (initialActiveLink) {
        initialActiveLink.classList.add('active');
    }
});