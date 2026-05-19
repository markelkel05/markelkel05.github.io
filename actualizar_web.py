import os
import sys
import json
import time
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: SUBIR IMÁGENES PARA ANÁLISIS VISUAL (AQUÍ ESTÁ LA MAGIA DE LAS SUBCARPETAS) ---
print("Buscando y subiendo imágenes para que la IA las analice visualmente...")
archivos_subidos_gemini = []
mapeo_imagenes_texto = ""

if os.path.exists("imagenes"):
    contador = 1
    # os.walk entra automáticamente en "imagenes" y en subcarpetas como "imagenes/programa"
    for ruta_raiz, carpetas, archivos in os.walk("imagenes"):
        for archivo in archivos:
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
                ruta_completa = os.path.join(ruta_raiz, archivo).replace("\\", "/")
                try:
                    # Al subir el archivo, le estamos dando "ojos" a la IA
                    archivo_gemini = client.files.upload(file=ruta_completa)
                    archivos_subidos_gemini.append(archivo_gemini)
                    mapeo_imagenes_texto += f"{contador}. Imagen visual adjunta -> Ruta a usar: '{ruta_completa}'\n"
                    contador += 1
                    print(f"Imagen {ruta_completa} subida con éxito.")
                except Exception as e:
                    print(f"Error subiendo la imagen {ruta_completa}: {e}")

# --- PASO 2: LEER CÓDIGO HTML ACTUAL DEL REPOSITORIO ---
textos_html_actuales = ""
for archivo in os.listdir("."):
    if os.path.isfile(archivo) and archivo.endswith(".html"):
        with open(archivo, "r", encoding="utf-8") as f:
            textos_html_actuales += f"\n\n--- CÓDIGO HTML ACTUAL: {archivo} ---\n{f.read()}\n"

# --- PASO 3: LEER CÓDIGO CSS Y JS ACTUAL ---
css_actual = ""
js_actual = ""
if os.path.exists("css/style.css"):
    with open("css/style.css", "r", encoding="utf-8") as f: css_actual = f.read()
if os.path.exists("js/script.js"):
    with open("js/script.js", "r", encoding="utf-8") as f: js_actual = f.read()

# --- PASO 4: CREAR EL PROMPT CON LIBERTAD CREATIVA PARA EL PARALLAX ---
print("Enviando todo el contexto a Gemini...")

prompt = f"""
CÓDIGO CSS ACTUAL (Diseño base futurista):
{css_actual}

CÓDIGO JS ACTUAL:
{js_actual}

CÓDIGO HTML ACTUAL DE LA WEB:
{textos_html_actuales}

INSTRUCCIONES DE ACTUALIZACIÓN OBLIGATORIAS:

INSTRUCCIONES DE ACTUALIZACIÓN OBLIGATORIAS:

1. **CONFIGURACIÓN DEL MENÚ (GENERAL):** - El menú debe contener EXACTAMENTE estos enlaces: "Solución Kentu", "IIOT para el mantenimiento", "Análisis OEE", "I+D+I", "Ayudas y subvenciones", "Contacto".
   - Destaca la página actual solo con cambio de color, sin subrayado permanente.

2. **LIBERTAD CREATIVA PARA FONDOS PARALLAX:**
   - Te he adjuntado varias imágenes. OBSÉRVALAS VISUALMENTE.
   - Quiero que decidas tú mismo qué imágenes encajan mejor como fondo (Parallax) para las cabeceras y separadores de las páginas (en este caso te permito hacer cambios a codigo ya prestablecido, pero por favor, mira bien las extensiones). 
   - Usa la lógica de diseño: elige imágenes oscuras, abstractas o de fábricas amplias para que el texto blanco se lea bien por encima. NO uses las capturas de pantalla del programa para los fondos Parallax.
   - Aplica las rutas que elijas en los `style="background-image: url('RUTA');"` de las secciones `.parallax-section`.
   - OBLIGATORIO: Asegúrate de que las imágenes elegidas aporten dinamismo a la web.
   - OBLIGATORIO PARA EVITAR PIXELADO: Para los fondos Parallax (cabeceras y separadores) utiliza ÚNICAMENTE imágenes que sepas que son de alta resolución o formato horizontal amplio (como 'iot-in-manufacturing-feat-image-scaled-1-1920x836.jpeg'). PROHIBIDO usar imágenes pequeñas, con resolución baja o nombres tipo '360_F_...' porque se pixelan al estirarse en la web.

3. **LIMPIEZA DE CONTENIDO:**
   - ELIMINA cualquier sección, apartado, div o galería dedicada a mostrar imágenes de la aplicación por ahora.
   - ELIMINA cualquier sección o etiqueta <video> que haya en el código.
   - ELIMINA del HTML, CSS y JS cualquier código relacionado con "Modales", "Lightboxes" o "Ventanas emergentes".
   - Quiero que dejes las páginas limpias, estructuradas únicamente con sus textos, tarjetas de servicios y diseño azul oscuro con los fondos Parallax que acabas de elegir.

4. **CORRECCIÓN DE TEXTOS (¡ESTRICTO!):**
   - En la página de mantenimiento (`mantenimiento.html`), busca el título que dice "Desde el desarrollo a pie de planta". 
   - REEMPLAZA OBLIGATORIAMENTE la palabra "planta" por "máquina". El texto final debe ser exactamente: "Desde el desarrollo a pie de máquina". 
   - Revisa también el resto del código: si aparece "pie de planta" en algún otro lado, cámbialo a "pie de máquina". No ignores esta regla.

5. **AÑADIR IMAGENES DETRAS DE LOS BOTONES**
    - En la página mantenimiento.html, hacia el final de la pagina, hay un apartado con el titulo "¿Quieres Verlo en Acción?" con un boton, quiero que ahí metas la imagen "MANTENIMIENTO_WORKING_PROGRAM (1).png".
    - En la página oee.html, hacia el final e la pagina, hay un apartado con el titulo "¿Listo para Aumentar la Productividad de tu Planta?" y un boton, detras de eso quiero que metas la imagen "OEE_ACTIVO (2).png".
    - IMPORTANTE: OBSÉRVA LAS IMÁGENES VISUALMENTE, los fondos de esta iagen son blancas, y quiero que sean más oscuros

Índice de rutas disponibles (úsalas para elegir los fondos):
{mapeo_imagenes_texto}

INSTRUCCIONES TÉCNICAS:
- Devuelve OBLIGATORIAMENTE LAS 4 PÁGINAS con su código COMPLETO en el JSON, desde <!DOCTYPE html> hasta el final.

{{
  "paginas": {{
    "index.html": "código html limpio aquí...",
    "mantenimiento.html": "código html limpio aquí...",
    "oee.html": "código html limpio aquí...",
    "contacto.html": "código html limpio aquí..."
  }},
  "css": "código css global limpio aquí",
  "js": "código javascript global limpio aquí"
}}
"""

contenido_multimodal = [prompt] + archivos_subidos_gemini

# --- PASO 5: PETICIÓN Y GUARDADO DINÁMICO (SISTEMA ANTI-CUELGUES) ---
max_reintentos = 3
codigo = None

for intento in range(max_reintentos):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contenido_multimodal,
            config={
                "response_mime_type": "application/json",
            }
        )
        codigo = json.loads(response.text.strip())
        break 
        
    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg and intento < max_reintentos - 1:
            print(f"Saturación de servidores (Error 503). Reintentando en 15s... (Intento {intento + 1}/{max_reintentos})")
            time.sleep(15)
        else:
            print(f"Error CRÍTICO: {e}")
            sys.exit(1)

if not codigo:
    print("Fallo tras varios reintentos.")
    sys.exit(1)

try:
    os.makedirs("css", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    
    paginas_generadas = codigo.get("paginas", {})
    
    if not paginas_generadas:
        print("Error: La IA no devolvió las páginas en el JSON.")
        sys.exit(1)
        
    for nombre_archivo, contenido_html in paginas_generadas.items():
        contenido_html += f"\n"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido_html)
        print(f"Guardado: {nombre_archivo} ({len(contenido_html)} caracteres)")
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Generación completada! La IA ha elegido los fondos y limpiado la web.")

except Exception as e:
    print(f"Error guardando archivos: {e}")
    sys.exit(1)