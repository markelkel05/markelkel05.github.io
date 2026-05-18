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

# --- PASO 2: LEER CÓDIGO ACTUAL ---
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
print("Enviando códigos e instrucciones para crear web multipágina a Gemini...")

prompt = f"""
CÓDIGO HTML ACTUAL (Inicio):
{html_actual}

CÓDIGO CSS ACTUAL:
{css_actual}

CÓDIGO JS ACTUAL:
{js_actual}

ARCHIVOS DE IMAGEN DISPONIBLES EN EL REPOSITORIO:
{texto_imagenes}

Generame nuevas paginas y metelas al menu.

INSTRUCCIONES EXCLUSIVAS PARA ESTA ACTUALIZACIÓN:
1. **NUEVAS PÁGINAS:** Separa el contenido en diferentes archivos HTML. Necesito que crees el código para estas páginas:
   - index.html (Página de inicio principal)
   - mantenimiento.html (Información sobre Mantenimiento IIOT)
   - oee.html (Análisis OEE)
   - contacto.html (Formulario e información de contacto)
2. **MENÚ DE NAVEGACIÓN:** En TODAS las páginas (HTMLs), actualiza la barra de navegación (menú) para que incluya enlaces funcionales a estas nuevas páginas (ej. <a href="mantenimiento.html">Mantenimiento</a>).
3. **DISEÑO PARALLAX:** Modifica el código para integrar las imágenes de la lista usando el efecto Parallax (background-attachment: fixed) en los fondos y separadores.
4. **ESTILOS DE TÍTULOS:** En la sección "Tecnología en el Corazón de Kentu", haz que todos los títulos de las etiquetas (por ejemplo: "Mantenimiento Predictivo Inteligente", "Informes Personalizados", "Integración Flexible", etc.) sean de color azul. Mantén el contenido del texto tal como está.
5. El CSS y JS deben ser globales y servir para todas las páginas creados sin romper la estructura visual previa. Manten la paleta azul oscuro futurista.

Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, añadiendo las claves para los nuevos archivos HTML:
{{
  "html_index": "código para index.html aquí",
  "html_mantenimiento": "código para mantenimiento.html aquí",
  "html_oee": "código para oee.html aquí",
  "html_contacto": "código para contacto.html aquí",
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
    
    # Asegurar que las carpetas de destino existen antes de escribir
    os.makedirs("css", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    
    # Guardar todos los archivos HTML por separado
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_index", ""))
        
    with open("mantenimiento.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_mantenimiento", ""))
        
    with open("oee.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_oee", ""))
        
    with open("contacto.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html_contacto", ""))
        
    # Guardar CSS y JS
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Sitio web multipágina generado con éxito!")

except Exception as e:
    print(f"Error en el proceso: {e}")
