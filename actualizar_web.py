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

Las etiquetas donde aparece el contenido, no se diferencian del fondo ue tienen, puedes hacer que tengan un fondo mas claaro (es decir, el fondo donde estan las etiquetas mantenlas asi,
pero el fondo del contenido de las etiquetas halo algo mas claro para que se puedan diferenciar)

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
