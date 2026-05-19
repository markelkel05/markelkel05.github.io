import os
import sys
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
carpetas_a_buscar = ["imagenes", "video", "videos"]
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

INSTRUCCIONES DE ACTUALIZACIÓN:
- Configuración general: En el menú de navegación, destaca la página actual en la que se encuentra el usuario (cambio de color al texto). Aplica esto en TODAS las páginas. Las imágenes Parallax deben incluir "IIOT" en su nombre y seguir el orden 4, 7 y 6 (o 4 y 7 si solo hay dos).
    
- Configuración de index.html: Añade dos fotos que empiecen con "OEE_" (Activo (2).png y HISTORICO.png), dos que empiecen con "MANTENIMIENTO_" (Working y Alarmas_Historico), la imagen de planificación, y la imagen "predictivo_plano" junto a "senal". NO CAMBIES EL TEXTO. Si es necesario, crea un apartado nuevo solo para las imágenes. Aplica un efecto CSS en estas imágenes para que se hagan MUCHO más grandes cuando el cursor pase por encima (efecto hover con transform: scale).
    
- Configuración de mantenimiento.html: Mete los dos vídeos que hay en esta página. NO CAMBIES EL CONTENIDO ACTUAL. Si es necesario, añade un nuevo apartado exclusivo para alojar los vídeos.
    
- Configuración de oee.html: No añadas imágenes aquí por ahora (se meterá un vídeo en el futuro). Solo actualiza lo del menú de navegación.

- Configuración de contacto.html: No modifiques el contenido, solo actualiza el menú de navegación.

INSTRUCCIONES TÉCNICAS:
1. MANTENIMIENTO: Usa el "CÓDIGO HTML ACTUAL" como base. Mantén la paleta azul oscuro.
2. VÍDEOS: Si es un vídeo de fondo usa `<video src="RUTA" autoplay loop muted playsinline>` con `object-fit: cover`. Si es explicativo usa `<video src="RUTA" controls>`.
3. PARALLAX: En el CSS usa siempre `background-attachment: fixed; background-size: cover; background-position: center; background-repeat: no-repeat;`.

IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON válido. Debes devolver obligatoriamente las 4 páginas en el JSON para que el menú se actualice en todas:
{{
  "paginas": {{
    "index.html": "código html actualizado aquí...",
    "mantenimiento.html": "código html actualizado aquí...",
    "oee.html": "código html actualizado aquí...",
    "contacto.html": "código html actualizado aquí..."
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
    
    # Comprobación de seguridad para saber si la IA ha devuelto páginas
    if not paginas_generadas:
        print("Error: La IA no ha devuelto ninguna página en el JSON.")
        sys.exit(1)
        
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
    # Ahora sí, si hay un error, GitHub se pondrá en rojo y nos avisará
    print(f"Error CRÍTICO en el proceso: {e}")
    sys.exit(1)
