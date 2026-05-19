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

INSTRUCCIONES DE ACTUALIZACIÓN OBLIGATORIAS (ANTI-PEREZA):
ATENCIÓN: Tu tarea principal es MODIFICAR EL HTML para añadir las etiquetas <img> y <video>. No devuelvas el mismo HTML de antes, DEBES insertar el nuevo contenido donde se te pide.

- Configuración general: En el menu necesito estos cambios: inicio -> Solución Kentu, Manenimiento -> IIOT para el mantenimiento, OEE Industrial -> Análisis OEE, añadir I+D+I, añadir Ayudas y subvenciones. Por ahora los añadidos no tienen pagina, pero muestralas. 
En las Imagenes Parallax, el orden tiene que ser IIOT_4.jpeg, IIOT_6.jpeg y si hay tres el siguiente es IIOT_7.jpeg. 
Hay un problema con el js, cada vez que se inicia una pagina, salta la ventana de las imagenes sin nada, solo quiero que esa ventana salga cuanndo se clickea una immagen.

- Configuración de index.html:
  1. Busca un buen lugar en el contenido y CREA un apartado nuevo para insertar imágenes.
  2. AÑADE etiquetas <img> con los nombres exactos que te paso: Usa "OEE_ACTIVO (2).png", "OEE_HISTORICO.png", "MANTENIMIENTO_WORKING_PROGRAM (1).png", "MANTENIMIENTO_ALARMAS_HISTORICO.png", "planificacion.png", "predictivo_plano.png" y "senal.png" (búscalas en el índice de rutas que tienes abajo).
  3. En el CSS de esta página, elimina lo que hace que con el hover se hagan mas grandes, pero manten que la etiqueta se destaque.
    
- Configuración de mantenimiento.html: CREA una sección nueva al final o donde encaje bien e INSERTA etiquetas <video> para los dos vídeos disponibles.
    
- Configuración de oee.html y contacto.html: Actualiza SOLO el menú de navegación.

INSTRUCCIONES TÉCNICAS:
1. MANTENIMIENTO: Mantiene el texto de los párrafos intacto, pero SÍ debes cambiar el código HTML para inyectar los videos y las fotos.
2. VÍDEOS: Si es un vídeo de fondo usa `<video src="RUTA" autoplay loop muted playsinline>` con `object-fit: cover`. Si es explicativo usa `<video src="RUTA" controls>`.
3. PARALLAX: En el CSS usa siempre `background-attachment: fixed; background-size: cover; background-position: center; background-repeat: no-repeat;`.

IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON válido. Debes devolver OBLIGATORIAMENTE LAS 4 PÁGINAS con su código COMPLETO, de principio a fin, sin recortar nada:
{{
  "paginas": {{
    "index.html": "código html COMPLETO y actualizado aquí...",
    "mantenimiento.html": "código html COMPLETO y actualizado aquí...",
    "oee.html": "código html COMPLETO y actualizado aquí...",
    "contacto.html": "código html COMPLETO y actualizado aquí..."
  }},
  "css": "código css global aquí",
  "js": "código javascript global aquí"
}}

Índice de imágenes adjuntas para saber las RUTAS EXACTAS:
{mapeo_imagenes_texto}
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
    
    if not paginas_generadas:
        print("Error: La IA no ha devuelto ninguna página en el JSON.")
        sys.exit(1)
        
    for nombre_archivo, contenido_html in paginas_generadas.items():
        # Añadimos un pequeño comentario oculto al final del HTML con cada ejecución
        # Esto OBLIGA a GitHub a detectar que el archivo HTML ha cambiado y forzar la subida
        contenido_html += f"\n<!-- Actualizado por IA -->"
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido_html)
        # El chivato nos dirá si la IA ha devuelto páginas vacías o con poco texto
        print(f"Página guardada con éxito: {nombre_archivo} (Tamaño: {len(contenido_html)} caracteres)")
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Generación completada! Imágenes y vídeos han sido integrados.")

except Exception as e:
    print(f"Error CRÍTICO en el proceso: {e}")
    sys.exit(1)
