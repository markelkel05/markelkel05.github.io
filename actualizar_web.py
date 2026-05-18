import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: CREAR CARPETAS ---
os.makedirs("css", exist_ok=True)
os.makedirs("js", exist_ok=True)

# --- PASO 2: LEER CÓDIGO ACTUAL (LA CLAVE DEL ÉXITO) ---
# Si ya tienes un diseño que te gusta, la IA necesita verlo para no romperlo.
html_actual = ""
css_actual = "
/* General Styles */
:root {
    --dark-blue: #0A0F18;
    --medium-blue: #1A2436;
    --accent-blue: #1E90FF;
    --light-blue: #ADD8E6;
    --text-white: #F8F8F8;
    --text-light-grey: #CCCCCC;
    --gradient-bg: linear-gradient(135deg, #0A0F18 0%, #1A2436 100%);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Poppins', sans-serif;
    line-height: 1.6;
    color: var(--text-light-grey);
    background: var(--dark-blue);
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif;
    color: var(--text-white);
    margin-bottom: 0.8em;
    line-height: 1.2;
}

h1 {
    font-size: 3.5em;
}

h2 {
    font-size: 2.5em;
    text-align: center;
    margin-bottom: 1.5em;
}

h3 {
    font-size: 1.8em;
}

p {
    margin-bottom: 1em;
}

a {
    color: var(--accent-blue);
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    color: var(--light-blue);
}

.btn {
    display: inline-block;
    padding: 12px 25px;
    border-radius: 5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    text-align: center;
    font-size: 0.9em;
}

.btn-primary {
    background-color: var(--accent-blue);
    color: var(--text-white);
}

.btn-primary:hover {
    background-color: var(--light-blue);
    color: var(--dark-blue);
}

.btn-secondary {
    background-color: transparent;
    border: 2px solid var(--accent-blue);
    color: var(--accent-blue);
}

.btn-secondary:hover {
    background-color: var(--accent-blue);
    color: var(--text-white);
}

/* Header */
.main-header {
    background-color: rgba(10, 15, 24, 0.9);
    position: fixed;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 1000;
    padding: 15px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.main-header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.8em;
    font-weight: 700;
    color: var(--text-white);
}

.logo span {
    color: var(--accent-blue);
}

.main-nav ul {
    list-style: none;
    display: flex;
}

.main-nav ul li {
    margin-left: 30px;
}

.main-nav ul li a {
    color: var(--text-light-grey);
    font-weight: 600;
    font-size: 1em;
    text-transform: uppercase;
    position: relative;
    padding: 5px 0;
}

.main-nav ul li a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: var(--accent-blue);
    transition: width 0.3s ease;
}

.main-nav ul li a:hover::after {
    width: 100%;
}

/* Burger Menu (for mobile) */
.burger-menu {
    display: none;
    flex-direction: column;
    cursor: pointer;
    padding: 5px;
}

.burger-menu span {
    height: 3px;
    width: 25px;
    background-color: var(--text-white);
    margin-bottom: 4px;
    border-radius: 2px;
    transition: all 0.3s ease;
}

/* Hero Section */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    color: var(--text-white);
    background-image: url('img/hero-kentu.jpg'); /* Placeholder image */
    background-size: cover;
    background-position: center;
    padding: 100px 0;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 900px;
    padding: 20px;
}

.hero h1 {
    font-size: 4.5em;
    margin-bottom: 0.3em;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
}

.hero p {
    font-size: 1.5em;
    margin-bottom: 2em;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.5);
}

.hero .btn {
    font-size: 1.1em;
    padding: 15px 35px;
}

/* Content Sections */
.content-section {
    padding: 80px 0;
    background-color: var(--medium-blue);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.content-section:nth-child(even) {
    background-color: var(--dark-blue);
}

.content-section p {
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    font-size: 1.1em;
    margin-bottom: 2em;
}

/* Grid Layouts */
.grid-3-cols {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    margin-top: 40px;
}

.grid-2-cols {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 30px;
    margin-top: 40px;
}

.feature-card, .advantage-card {
    background-color: var(--dark-blue);
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    transition: transform 0.3s ease, background-color 0.3s ease;
}

.feature-card:hover, .advantage-card:hover {
    transform: translateY(-5px);
    background-color: var(--medium-blue);
}

.feature-card h3, .advantage-card h3 {
    color: var(--accent-blue);
    margin-bottom: 10px;
    font-size: 1.5em;
}

.feature-item {
    background-color: var(--dark-blue);
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.feature-item:hover {
    transform: translateY(-3px);
}

.feature-item h3 {
    color: var(--accent-blue);
    font-size: 1.3em;
    margin-bottom: 8px;
}

.feature-item p {
    text-align: left;
    font-size: 1em;
    margin-bottom: 0;
}

/* Parallax Sections */
.parallax-section {
    background-attachment: fixed;
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
}

.parallax-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1;
}

.parallax-separator {
    height: 50vh; /* Adjust height for separation */
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-white);
    text-align: center;
}

.separator-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    padding: 20px;
}

.separator-content h2 {
    font-size: 3em;
    margin-bottom: 0;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
}

/* CTA Section */
.cta-section {
    background: var(--gradient-bg);
    padding: 100px 0;
    text-align: center;
}

.cta-section h2 {
    color: var(--text-white);
    font-size: 3em;
    margin-bottom: 0.5em;
}

.cta-section p {
    font-size: 1.3em;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 2.5em;
}

.cta-section .btn {
    margin: 0 10px;
    font-size: 1.1em;
    padding: 15px 35px;
}

/* Footer */
.main-footer {
    background-color: var(--dark-blue);
    color: var(--text-light-grey);
    padding: 60px 0 30px;
    font-size: 0.9em;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    margin-bottom: 40px;
}

.footer-col h3 {
    color: var(--text-white);
    font-size: 1.2em;
    margin-bottom: 1em;
}

.footer-col ul {
    list-style: none;
}

.footer-col ul li {
    margin-bottom: 8px;
}

.footer-col ul li a {
    color: var(--text-light-grey);
    transition: color 0.3s ease;
}

.footer-col ul li a:hover {
    color: var(--accent-blue);
}

.social-links {
    margin-top: 15px;
    display: flex;
    gap: 15px;
}

.social-links img {
    width: 28px;
    height: 28px;
    opacity: 0.7;
    transition: opacity 0.3s ease;
}

.social-links img:hover {
    opacity: 1;
}

.copyright {
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 20px;
}

/* Responsive Design */
@media (max-width: 992px) {
    .main-nav {
        display: none;
    }

    .burger-menu {
        display: flex;
    }

    .main-nav.active {
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background-color: var(--dark-blue);
        box-shadow: 0 5px 10px rgba(0,0,0,0.3);
    }

    .main-nav.active ul {
        flex-direction: column;
        text-align: center;
        padding: 20px 0;
    }

    .main-nav.active ul li {
        margin: 10px 0;
    }

    .hero h1 {
        font-size: 3em;
    }

    .hero p {
        font-size: 1.2em;
    }

    h2 {
        font-size: 2em;
    }

    .parallax-separator h2 {
        font-size: 2.2em;
    }

    .cta-section h2 {
        font-size: 2.5em;
    }

    .grid-3-cols, .grid-2-cols {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.5em;
    }

    .hero p {
        font-size: 1em;
    }

    .hero .btn {
        padding: 10px 25px;
        font-size: 1em;
    }

    h2 {
        font-size: 1.8em;
    }

    .parallax-separator h2 {
        font-size: 1.8em;
    }

    .cta-section h2 {
        font-size: 2em;
    }

    .cta-section .btn {
        margin: 10px 0;
        width: 80%;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    .footer-grid {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .footer-col ul {
        padding-left: 0;
    }

    .social-links {
        justify-content: center;
    }
}"
js_actual = "
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
            }
        });
    }
});
"

try:
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f: html_actual = f.read()
    if os.path.exists("css/style.css"):
        with open("css/style.css", "r", encoding="utf-8") as f: css_actual = f.read()
    if os.path.exists("js/script.js"):
        with open("js/script.js", "r", encoding="utf-8") as f: js_actual = f.read()
except Exception as e:
    print(f"No se pudo leer el código anterior: {e}")

# --- PASO 3: GENERAR LA WEB CON GEMINI ---
print("Generando/Actualizando el código de la web...")

# RELLENA ESTO: Pon aquí los nombres exactos y rutas de tus fotos
lista_de_imagenes = """
- Ruta: 'imagenes/parallax1.jpg' (Usar para la cabecera principal)
- Ruta: 'imagenes/parallax2.jpg' (Usar como separador entre servicios y contacto)
"""

prompt = f"""
Eres un desarrollador web experto. Tu tarea es actualizar y mejorar una página web para Kentu (empresa de IIOT).

CÓDIGO ACTUAL (MANTÉN ESTA ESTRUCTURA INTACTA, NO ROMPAS EL DISEÑO VISUAL):
HTML:
{html_actual if html_actual else "No hay HTML previo. Crea uno nuevo con diseño futurista azul oscuro tipo Baliatekks.com"}

CSS:
{css_actual if css_actual else "No hay CSS previo. Crea uno nuevo."}

JS:
{js_actual if js_actual else "No hay JS previo."}

INSTRUCCIONES DE ACTUALIZACIÓN:
1. Necesito que añadas las siguientes imágenes utilizando un efecto Parallax amplio (background-attachment: fixed).
2. Estas son las rutas exactas de las imágenes que DEBES usar en los atributos background-image del CSS o en etiquetas HTML según convenga:
{lista_de_imagenes}
3. Acomoda las imágenes en los fondos de las cabeceras y como separadores de contenido.
4. Si la estructura actual ya está bien, SOLO añade el CSS y el HTML necesario para el efecto Parallax. No cambies tipografías, colores ni el layout general si ya te he pasado código actual.

REQUISITO TÉCNICO:
Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, sin comillas Markdown:
{{
  "html": "código html aquí",
  "css": "código css aquí",
  "js": "código javascript aquí"
}}
"""

try:
    # Usamos response_mime_type para forzar a la IA a devolver un JSON puro
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            "response_mime_type": "application/json",
        }
    )

    respuesta_texto = response.text.strip()
    codigo = json.loads(respuesta_texto)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html", ""))
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Código generado y archivos guardados con éxito con efecto Parallax!")

except json.JSONDecodeError:
    print("Error: La IA no devolvió un formato JSON válido.")
    print("Respuesta cruda:", respuesta_texto)
except Exception as e:
    print(f"Error al generar la web: {e}")
    print("Nota: Si el error menciona '503 UNAVAILABLE', los servidores están muy ocupados en este momento. Espera unos minutos.")
