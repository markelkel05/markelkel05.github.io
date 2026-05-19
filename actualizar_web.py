import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: SUBIR IMÁGENES PARA ANÁLISIS VISUAL ---
print("Subiendo imágenes para que la IA las analice visualmente...")
archivos_subidos_gemini = []
mapeo_imagenes_texto = ""

if os.path.exists("imagenes"):
    contador = 1
    for archivo in os.listdir("imagenes"):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
            ruta_completa = os.path.join("imagenes", archivo).replace("\\", "/")
            try:
                archivo_gemini = client.files.upload(file=ruta_completa)
                archivos_subidos_gemini.append(archivo_gemini)
                mapeo_imagenes_texto += f"{contador}. Imagen visual adjunta -> Ruta a usar: '{ruta_completa}'\n"
                contador += 1
                print(f"Imagen {ruta_completa} subida con éxito.")
            except Exception as e:
                print(f"Error subiendo la imagen {ruta_completa}: {e}")

# --- PASO 2: DETECTAR VÍDEOS EN EL REPOSITORIO ---
print("Buscando archivos de vídeo...")
mapeo_videos_texto = ""
# Buscamos vídeos tanto en "imagenes" como en una posible carpeta "videos"
carpetas_a_buscar = ["imagenes", "videos"]
for carpeta in carpetas_a_buscar:
    if os.path.exists(carpeta):
        for archivo in os.listdir(carpeta):
            if archivo.lower().endswith(('.mp4', '.webm', '.ogg')):
                ruta_completa = os.path.join(carpeta, archivo).replace("\\", "/")
                mapeo_videos_texto += f"- Vídeo disponible: '{ruta_completa}'\n"
                print(f"Vídeo detectado: {ruta_completa}")

if not mapeo_videos_texto:
    mapeo_videos_texto = "No se han detectado archivos de vídeo."

# --- PASO 3: LEER CÓDIGO HTML ACTUAL DEL REPOSITORIO ---
textos_html_actuales = ""
for archivo in os.listdir("."):
    if os.path.isfile(archivo) and archivo.endswith(".html"):
        with open(archivo, "r", encoding="utf-8") as f:
            textos_html_actuales += f"\n\n--- CÓDIGO HTML ACTUAL: {archivo} ---\n{f.read()}\n"

# --- PASO 4: LEER CÓDIGO CSS Y JS ACTUAL ---
css_actual = ""
js_actual = ""
if os.path.exists("css/style.css"):
    with open("css/style.css", "r", encoding="utf-8") as f: css_actual = f.read()
if os.path.exists("js/script.js"):
    with open("js/script.js", "r", encoding="utf-8") as f: js_actual = f.read()

# --- PASO 5: CREAR EL PROMPT CON TEXTO, IMÁGENES Y VÍDEOS ---
print("Enviando todo el contexto (Código + Imágenes + Vídeos) a Gemini...")

prompt = f"""
CÓDIGO CSS ACTUAL (Diseño base futurista):
{css_actual}

CÓDIGO JS ACTUAL:
{js_actual}

CÓDIGO HTML ACTUAL DE LA WEB:
{textos_html_actuales}

VÍDEOS DISPONIBLES EN EL REPOSITORIO:
{mapeo_videos_texto}

INSTRUCCIONES EXCLUSIVAS Y ANÁLISIS VISUAL:
1. **MANTENIMIENTO DE CONTENIDO:** Usa el "CÓDIGO HTML ACTUAL" como base. Mantén los textos, la paleta azul oscuro y la estructura, pero mejora la maquetación.
2. **USO DE IMÁGENES:** Analiza las imágenes que te he adjuntado visualmente. Usa las más amplias/oscuras para fondos Parallax y las más técnicas para acompañar textos.
   Índice de imágenes adjuntas para las rutas:
   {mapeo_imagenes_texto}
3. **INTEGRACIÓN DE VÍDEOS (NUEVO):** Tienes una lista de vídeos disponibles. Úsalos inteligentemente en el código HTML. 
   - Si por el nombre del archivo parece un vídeo de fondo o ambiente, ponlo como fondo de una sección (detrás del texto) usando la etiqueta HTML5: `<video src="RUTA" autoplay loop muted playsinline></video>` con el CSS necesario para que cubra el fondo (`object-fit: cover`).
   - Si parece un vídeo explicativo o demo, ponlo dentro del contenido con controles: `<video src="RUTA" controls></video>`.
4. **DISEÑO PARALLAX SIN PIXELAR:** En el CSS de las imágenes de fondo usa siempre: `background-attachment: fixed; background-size: cover; background-position: center; background-repeat: no-repeat;`.
5. **MENÚ DE NAVEGACIÓN:** Unifica el menú para que conecte de forma coherente todas las páginas HTML.

Devuelve ÚNICAMENTE un objeto JSON válido con la estructura:
{{
  "paginas": {{
    "index.html": "código html actualizado aquí...",
    "mantenimiento.html": "código html actualizado aquí..."
  }},
  "css": "código css global aquí",
  "js": "código javascript global aquí"
}}
"""

contenido_multimodal = [prompt] + archivos_subidos_gemini

# --- PASO 6: PETICIÓN Y GUARDADO DINÁMICO ---
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contenido_multimodal,
        config={
            "response_mime_type": "application/json",
        }
    )
    codigo = json.loads(response.text.strip())
    
    os.makedirs("css", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    
    paginas_generadas = codigo.get("paginas", {})
    for nombre_archivo, contenido_html in paginas_generadas.items():
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido_html)
        print(f"Página guardada con éxito: {nombre_archivo}")
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Generación completada! Imágenes y vídeos han sido integrados.")

except Exception as e:
    print(f"Error en el proceso: {e}")
