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
css_actual = ""
js_actual = ""

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
