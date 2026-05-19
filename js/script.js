document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const offsetTop = targetElement.getBoundingClientRect().top + window.pageYOffset;
                // Adjust for fixed header height if necessary
                const headerHeight = document.querySelector('.main-header').offsetHeight;
                window.scrollTo({
                    top: offsetTop - headerHeight - 20, // Added some extra padding
                    behavior: 'smooth'
                });
            }
        });
    });

    // Hamburger menu functionality
    const burgerMenu = document.querySelector('.burger-menu');
    const mainNav = document.querySelector('.main-nav');

    if (burgerMenu) {
        burgerMenu.addEventListener('click', () => {
            mainNav.classList.toggle('active');
            burgerMenu.classList.toggle('active'); // Optional: Add a class for animating burger icon
        });

        // Close menu when a nav link is clicked (for mobile)
        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (mainNav.classList.contains('active')) {
                    mainNav.classList.remove('active');
                    burgerMenu.classList.remove('active');
                }
            });
        });
    }

    // Optional: Add a class to header on scroll for styling changes (e.g., background blur, shadow)
    const header = document.querySelector('.main-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            };
        });
    };

    // NEW: Highlight active navigation link
    const currentPath = window.location.pathname.split('/').pop(); // Get filename (e.g., "index.html")
    const navLinks = document.querySelectorAll('.main-nav ul li a');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href').split('/').pop();
        // Handle empty path for index.html (e.g., when visiting root URL ")
        if (currentPath === linkPath || (currentPath === '' && linkPath === 'index.html')) {
            link.classList.add('current-page');
        }
    });

    // NEW: Image Lightbox functionality
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const span = document.getElementsByClassName("modal-close")[0];

    document.querySelectorAll('.gallery-image').forEach(img => {
        img.addEventListener('click', function(){
            modal.style.display = "flex"; // Use flex to center
            modalImg.src = this.src;
            modalImg.alt = this.alt;
        });
    });

    if (span) {
        span.addEventListener('click', () => {
            modal.style.display = "none";
        });
    }

    // Close modal when clicking outside of the image
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = "none";
            }
        });
    }
});