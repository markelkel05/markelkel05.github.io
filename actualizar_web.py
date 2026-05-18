import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: DETECTAR IMÁGENES EN EL REPOSITORIO ---
carpeta_imagenes = "imagenes" 
imagenes_disponibles = []

if os.path.exists(carpeta_imagenes):
    for archivo in os.listdir(carpeta_imagenes):
        # Filtramos solo archivos de imagen comunes
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
            ruta_completa = os.path.join(carpeta_imagenes, archivo)
            imagenes_disponibles.append(ruta_completa)

# Convertimos la lista de rutas a un texto limpio para el prompt
texto_imagenes = "\n".join([f"- {img}" for img in imagenes_disponibles])

# --- PASO 2: LEER CÓDIGO ACTUAL ---
# Corregido: Inicializar como texto vacío para evitar errores si el archivo no existe
html_actual = ""
css_actual = ""
js_actual = ""

if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f: html_actual = f.read()
if os.path.exists("css/style.css"):
    with open("css/style.css", "r", encoding="utf-8") as f: css_actual = f.read()
if os.path.exists("js/script.js"):
    with open("js/script.js", "r", encoding="utf-8") as f: js_actual = f.read()


# --- PASO 3: CREAR EL PROMPT PURO DE CÓDIGO ---
print("Enviando códigos y nombres de imágenes a Gemini...")

# Aquí está la corrección: Las llaves sueltas ahora son dobles (}})
prompt = f"""
CÓDIGO HTML ACTUAL:
{html_actual}

CÓDIGO CSS ACTUAL:
{css_actual}

CÓDIGO JS ACTUAL:
{js_actual}

ARCHIVOS DE IMAGEN DISPONIBLES EN EL REPOSITORIO:
{texto_imagenes}

En una de las versiones anterires, hay este codigo de HTML:  <section id="hero" class="hero parallax-section" style="background-image: url('IIOT_Prueba.jpeg');">
            <div class="hero-content">
                <h1 class="hero-title">Kentu: Impulsando la Excelencia en la Industria 4.0</h1>
                <p class="hero-subtitle">Transforma tu mantenimiento y optimiza el OEE con nuestra solución IIOT de vanguardia.</p>
                <a href="#solutions" class="btn btn-primary">Descubre Nuestras Soluciones</a>
            </div>
        </section>

        <section id="solutions" class="content-section">
            <div class="container">
                <h2 class="section-title">Nuestras Soluciones IIOT</h2>
                <p class="section-description">Hemos desarrollado un programa innovador para revolucionar el mantenimiento industrial y la Eficiencia General de los Equipos (OEE).</p>
                <div class="solutions-grid">
                    <div class="solution-card">
                        <h3>Mantenimiento Predictivo Inteligente</h3>
                        <p>Anticípate a fallos con algoritmos avanzados de IA y ML. Reduce el tiempo de inactividad no planificado y optimiza la vida útil de tus activos.</p>
                    </div>
                    <div class="solution-card">
                        <h3>Optimización OEE en Tiempo Real</h3>
                        <p>Monitoriza cada aspecto de tus máquinas: disponibilidad, rendimiento y calidad. Identifica cuellos de botella y maximiza la productividad al instante.</p>
                    </div>
                    <div class="solution-card">
                        <h3>Análisis de Datos Profundo</h3>
                        <p>Recopila y analiza datos de máquinas para obtener insights accionables. Toma decisiones basadas en información precisa para una mejora continua.</p>
                    </div>
                    <div class="solution-card">
                        <h3>Integración y Escalabilidad</h3>
                        <p>Nuestra plataforma se integra sin problemas con tus sistemas existentes y es escalable para crecer con tus operaciones, desde una línea hasta toda la planta.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Parallax Section 1 -->
        <section class="parallax-section parallax-1">
            <div class="parallax-overlay">
                <h2>Visualiza el futuro de tu planta</h2>
                <p>Donde cada máquina te habla y cada dato cuenta una historia de eficiencia.</p>
            </div>
        </section>

        <section id="technology" class="content-section">
            <div class="container">
                <h2 class="section-title">Tecnología en el Corazón de Kentu</h2>
                <p class="section-description">Nuestra plataforma se basa en la última tecnología IIOT para ofrecerte precisión, fiabilidad y rendimiento inigualable.</p>
                <div class="tech-features">
                    <div class="tech-item">
                        <i class="fas fa-microchip icon"></i>
                        <h3>Sensores Inteligentes</h3>
                        <p>Recopilación de datos en tiempo real de temperatura, vibración, presión y más.</p>
                    </div>
                    <div class="tech-item">
                        <i class="fas fa-cloud icon"></i>
                        <h3>Plataforma Cloud Segura</h3>
                        <p>Almacenamiento y procesamiento de datos en la nube con máxima seguridad y accesibilidad.</p>
                    </div>
                    <div class="tech-item">
                        <i class="fas fa-robot icon"></i>
                        <h3>IA y Machine Learning</h3>
                        <p>Algoritmos predictivos que aprenden de tus máquinas para anticipar problemas.</p>
                    </div>
                    <div class="tech-item">
                        <i class="fas fa-chart-line icon"></i>
                        <h3>Dashboards Intuitivos</h3>
                        <p>Visualización clara y personalizable de tus métricas clave y estado de equipos.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Parallax Section 2 -->
        <section class="parallax-section parallax-2">
            <div class="parallax-overlay">
                <h2>Desde el desarrollo a pie de planta</h2>
                <p>Entendemos tus desafíos porque los hemos vivido. Creamos soluciones para ti, por ti.</p>
            </div>
        </section>

        <section id="about" class="content-section">
            <div class="container">
                <h2 class="section-title">Sobre Kentu: Desarrolladores a Pie de Planta</h2>
                <p class="section-description">En Kentu, no somos solo desarrolladores; somos ingenieros con experiencia directa en el entorno industrial. Entendemos las complejidades del taller, las presiones de la producción y la necesidad de soluciones que realmente funcionen. Nuestro programa IIOT nació de la necesidad de herramientas robustas y eficaces que nosotros mismos queríamos tener.</p>
                <div class="about-vision">
                    <h3>Nuestra Visión</h3>
                    <p>Ser el socio tecnológico líder para la industria, impulsando la eficiencia operativa y la sostenibilidad a través de la innovación IIOT.</p>
                </div>
            </div>
        </section>/// Lo qeu pasa es que preferimos la estructura actual del HTML, sin embargo preferimos el contenido del codigo que te esto diciendo.
Haz una mezcla de la estructura que tenemos (de ai manten las fotos con el efecto Parallax) y el contenido del HTML que te estoy diciendo

}}
Informes Personalizados
Genera informes detallados sobre el rendimiento, el consumo energético y las tendencias de mantenimiento.

Integración Flexible
Compatible con una amplia gama de equipos y sistemas existentes en tu línea de producción.), soluciona el problema

INSTRUCCIONES EXCLUSIVAS:
1. Modifica el código anterior para integrar las imágenes de la lista usando el efecto Parallax (background-attachment: fixed).
2. No elimines secciones, no cambies los textos ni alteres la paleta de colores azul oscuro futurista que ya existe. Solo añade el diseño Parallax usando las rutas exactas provistas.
3. El CSS y JS deben mantener la compatibilidad para que nada de la estructura visual previa se rompa.

Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta:
{{
  "html": "código html modificado aquí",
  "css": "código css modificado aquí",
  "js": "código javascript modificado aquí"
}}
"""

# --- PASO 4: PETICIÓN Y GUARDADO ---
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            "response_mime_type": "application/json",
        }
    )

    codigo = json.loads(response.text.strip())
    
    # Asegurar que las carpetas de destino existen antes de escribir
    os.makedirs("css", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html", ""))
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Página web actualizada con éxito incorporando las imágenes!")

except Exception as e:
    print(f"Error en el proceso: {e}")
