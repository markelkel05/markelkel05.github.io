import os
import sys
import json
import time
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: RECOPILAR RUTAS DE IMÁGENES (SIN SUBIR A LA IA) ---
print("Buscando rutas de imágenes para pasarlas como texto...")
mapeo_imagenes_texto = ""

if os.path.exists("imagenes"):
    contador = 1
    for ruta_raiz, carpetas, archivos in os.walk("imagenes"):
        for archivo in archivos:
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
                ruta_completa = os.path.join(ruta_raiz, archivo).replace("\\", "/")
                mapeo_imagenes_texto += f"{contador}. Ruta disponible: '{ruta_completa}'\n"
                contador += 1
                
print(f"Se encontraron {contador - 1} imágenes. Rutas guardadas en memoria.")

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

1. **CONFIGURACIÓN DEL MENÚ (GENERAL):** - El menú debe contener EXACTAMENTE estos enlaces: "Solución Kentu", "IIOT para el mantenimiento", "Análisis OEE", "I+D+I", "Ayudas y subvenciones", "Contacto".
   - Destaca la página actual solo con cambio de color, sin subrayado permanente.

2. **LIBERTAD CREATIVA PARA FONDOS PARALLAX (Este paso ya esta mplementado a nuestro gusto, saltatelo, no hagas este paso):**
   - Te he proporcionado un listado de rutas de imágenes disponibles más abajo.
   - Quiero que decidas tú mismo qué imágenes encajan mejor como fondo (Parallax) para las cabeceras y separadores de las páginas. 
   - Usa la lógica de diseño: elige imágenes oscuras, abstractas o de fábricas amplias para que el texto blanco se lea bien por encima. NO uses las capturas de pantalla del programa.
   - Aplica las rutas en los `style="background-image: url('RUTA');"` de las secciones `.parallax-section`.
   - OBLIGATORIO: Utiliza ÚNICAMENTE imágenes que por su nombre intuyas que son de alta resolución amplias. PROHIBIDO usar imágenes pequeñas.

3. **LIMPIEZA DE CONTENIDO:**
   - ELIMINA cualquier sección, apartado, div o galería dedicada a mostrar imágenes de la aplicación por ahora.
   - ELIMINA cualquier sección o etiqueta <video>.
   - ELIMINA del HTML, CSS y JS cualquier código relacionado con "Modales", "Lightboxes" o "Ventanas emergentes".
   - Deja las páginas limpias, estructuradas únicamente con sus textos, tarjetas de servicios y diseño azul oscuro con fondos Parallax.

4. **CORRECCIÓN DE TEXTOS (¡ESTRICTO!):**
   - En `mantenimiento.html`, busca el título "Desde el desarrollo a pie de planta". 
   - REEMPLAZA OBLIGATORIAMENTE "planta" por "máquina". (Texto final: "Desde el desarrollo a pie de máquina"). 
   - Cambia "pie de planta" por "pie de máquina" en todo el código si vuelve a aparecer.

5. **AÑADIR IMÁGENES DETRÁS DE LOS BOTONES:**
    - En `mantenimiento.html`, apartado "¿Quieres Verlo en Acción?", mete la imagen "MANTENIMIENTO_WORKING_PROGRAM (1).png".
    - En `oee.html`, apartado "¿Listo para Aumentar la Productividad...?", mete la imagen "OEE_ACTIVO (2).png".
    - IMPORTANTE: Integra CSS en esas secciones para que el fondo de esas imágenes quede visualmente más oscuro y se integre con la web.

6. **REGLA CRÍTICA DE FORMATO JSON (ANTI-CRASHEOS):**
   - Tu respuesta debe ser un JSON estrictamente válido.
   - ¡MUY IMPORTANTE! Para evitar romper el JSON, SUSTITUYE TODAS LAS COMILLAS DOBLES (") de tu código HTML y CSS por COMILLAS SIMPLES (').
   - Escribe `<div class='parallax-section'>` en lugar de `<div class="parallax-section">`.
   - Si tienes que usar comillas dobles, escápalas obligatoriamente con `\\\"`.

Índice de rutas disponibles:
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

# --- PASO 5: PETICIÓN Y GUARDADO DINÁMICO (SISTEMA ANTI-CUELGUES) ---
max_reintentos = 3
codigo = None

for intento in range(max_reintentos):
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            }
        )
        
        # Limpieza de bloques de código markdown que a veces la IA mete por error
        texto_ia = response.text.strip()
        if texto_ia.startswith("```json"):
            texto_ia = texto_ia[7:]
        if texto_ia.startswith("```"):
            texto_ia = texto_ia[3:]
        if texto_ia.endswith("```"):
            texto_ia = texto_ia[:-3]
            
        # strict=False ayuda a tolerar pequeños errores de saltos de línea
        codigo = json.loads(texto_ia.strip(), strict=False)
        break 
        
    except json.JSONDecodeError as e:
        print(f"Error de formato JSON en el intento {intento + 1}: {e}")
        if intento < max_reintentos - 1:
            print("Reintentando para que la IA genere un formato limpio...")
            time.sleep(5)
        else:
            print("Error CRÍTICO: La IA falló repetidamente al generar un JSON válido.")
            # Guardamos el texto roto para poder leerlo y ver dónde se equivocó la IA
            with open("error_json_ia.txt", "w", encoding="utf-8") as f:
                f.write(texto_ia)
            print("Se ha guardado 'error_json_ia.txt' con la respuesta errónea para revisar.")
            sys.exit(1)
            
    except Exception as e:
        error_msg = str(e)
        if "503" in error_msg and intento < max_reintentos - 1:
            print(f"Saturación de servidores. Reintentando... (Intento {intento + 1}/{max_reintentos})")
            time.sleep(15)
        else:
            print(f"Error CRÍTICO de conexión o de la API: {e}")
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
        
    print("¡Generación completada! La IA ha actualizado la web sin errores de formato.")

except Exception as e:
    print(f"Error guardando los archivos finales: {e}")
    sys.exit(1)