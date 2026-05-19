import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: DETECTAR IMÁGENES EN EL REPOSITORIO ---
carpeta_imagenes = "imagenes" 
imagenes_disponibles = []

if os.path.exists(carpeta_imagenes):
    for archivo in os.listdir(carpeta_imagenes):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
            ruta_completa = os.path.join(carpeta_imagenes, archivo)
            imagenes_disponibles.append(ruta_completa)

texto_imagenes = "\n".join([f"- {img}" for img in imagenes_disponibles])

# --- PASO 2: LEER CÓDIGO ACTUAL DE TODAS LAS PÁGINAS ---
# Inicializamos todas las variables vacías por si es la primera ejecución
html_index_actual = ""
html_mantenimiento_actual = ""
html_oee_actual = ""
html_contacto_actual = ""
css_actual = ""
js_actual = ""

if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f: html_index_actual = f.read()
if os.path.exists("mantenimiento.html"):
    with open("mantenimiento.html", "r", encoding="utf-8") as f: html_mantenimiento_actual = f.read()
if os.path.exists("oee.html"):
    with open("oee.html", "r", encoding="utf-8") as f: html_oee_actual = f.read()
if os.path.exists("contacto.html"):
    with open("contacto.html", "r", encoding="utf-8") as f: html_contacto_actual = f.read()
if os.path.exists("css/style.css"):
    with open("css/style.css", "r", encoding="utf-8") as f: css_actual = f.read()
if os.path.exists("js/script.js"):
    with open("js/script.js", "r", encoding="utf-8") as f: js_actual = f.read()

# --- PASO 3: CREAR EL PROMPT CON TODO EL CONTEXTO ---
print("Enviando todos los códigos de la web multipágina e imágenes a Gemini...")

prompt = f"""
CÓDIGO HTML ACTUAL (index.html):
{html_index_actual}

CÓDIGO HTML ACTUAL (mantenimiento.html):
{html_mantenimiento_actual}

CÓDIGO HTML ACTUAL (oee.html):
{html_oee_actual}

CÓDIGO HTML ACTUAL (contacto.html):
{html_contacto_actual}

CÓDIGO CSS ACTUAL:
{css_actual}

CÓDIGO JS ACTUAL:
{js_actual}

ARCHIVOS DE IMAGEN DISPONIBLES EN EL REPOSITORIO:
{texto_imagenes}

- Cambios en general: He metido unas nuevas imagenes (del 4 a 6 antes de la extension de archivos) ue son mas grandes que el resto, cambialas por las immagenes que ya hay puestas para qu no se vean pixeladas
- Cambios para index.html:
- Cambios para mantenimiento.html:
- Cambios para oee.html:
- Cambios para contacto.html: 

INSTRUCCIONES EXCLUSIVAS PARA ESTA ACTUALIZACIÓN:
1. **MANTENER MULTIPÁGINA:** Revisa y actualiza los archivos HTML provistos. Si ya existen, mantén sus estructuras básicas y mejora su contenido basándote en lo que ya tienen escrito.
2. **MENÚ DE NAVEGACIÓN:** Asegúrate de que en TODAS las páginas (HTMLs), la barra de navegación (menú) tenga los enlaces funcionales correctos entre ellas.
3. **DISEÑO PARALLAX SIN PIXELAR:** Integra las imágenes de la lista usando el efecto Parallax. Para evitar que las imágenes se vean pixeladas, estiradas o deformadas, aplica obligatoriamente estas propiedades en el CSS de cada fondo:
   - `background-attachment: fixed;`
   - `background-size: cover;` (Esto hace que la imagen se adapte de forma inteligente al tamaño de la pantalla sin deformarse).
   - `background-position: center;` (Centra la imagen para que se vea lo más importante).
   - `background-repeat: no-repeat;`
4. **ESTILOS DE TÍTULOS:** En la sección "Tecnología en el Corazón de Kentu" (o secciones equivalentes de características), haz que todos los títulos de las etiquetas (por ejemplo: "Mantenimiento Predictivo Inteligente", "Informes Personalizados", "Integración Flexible", etc.) sean de color azul. Mantén el contenido del texto tal como está.
5. El CSS y JS deben seguir siendo globales, óptimos para todas las páginas y mantener la estética azul oscura futurista.

Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta:
{{
  "html_index": "código para index.html modificado aquí",
  "html_mantenimiento": "código para mantenimiento.html modificado aquí",
  "html_oee": "código para oee.html modificado aquí",
  "html_contacto": "código para contacto.html modificado aquí",
  "css": "código css global modificado aquí",
  "js": "código javascript global modificado aquí"
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
    
    os.makedirs("css", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_index", ""))
        
    with open("mantenimiento.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_mantenimiento", ""))
        
    with open("oee.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_oee", ""))
        
    with open("contacto.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_contacto", ""))
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Sitio web multipágina actualizado con éxito manteniendo todo el contexto!")

except Exception as e:
    print(f"Error en el proceso: {e}")
