import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: CREAR CARPETAS ---
os.makedirs("css", exist_ok=True)
os.makedirs("js", exist_ok=True)

# --- PASO 2: GENERAR LA WEB CON GEMINI ---
print("Generando el código de la web...")
prompt = """
Eres un desarrollador web experto. Crea una página web para una empresa de IIOT (Industrial Internet of Things) para la empresa Kentu, que ha generado un nuevo programa para el mantenimiento y el OEE de las máquinas. 
Somos desarrolladores a pie de planta. El diseño debe ser futurista, similar (casi igual) a "www.Baliatekks.com", con azul oscuro como color principal.

Necesito que añadas las imagenes que hay en el repositorio con el efecto Parallax al HTML, pero no rompas la estructura, se ve bien, si vas a cambiar algo, arreglalo cambiando el css o js para que siga siendo visible,
POR FAVOR AÑADE LAS IMMAGENES DONDE SE DEBEN (El titulo y las separaciones entre contenido, donde estan las cabeceras).

IMPORTANTE: 
1. Divide el código en HTML, CSS y JavaScript.
2. El HTML DEBE estar enlazado a las carpetas correctas: <link rel="stylesheet" href="css/style.css"> y <script src="js/script.js"></script>.
3. REQUISITO PARALLAX: Incluye secciones con Efecto Parallax amplio (background-attachment: fixed).
4. Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, sin comillas Markdown:
{
  "html": "código html aquí",
  "css": "código css aquí",
  "js": "código javascript aquí"
}
5. Si te digo que la estructura esta bien, no cambies como se ve, solo añade lo que te pida y (si es necesario) haz cambios para que al visualizarlo se vea commo esaba antes con e contenido añadido.
  Lo mismo pasa con el contenido, a menos de que te diga de cambiar el contenido, no lo cambies (a contenido le digo lo que se muestra en modo texto en la página.
"""

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    respuesta_texto = response.text.strip()

    # Limpieza de seguridad
    if respuesta_texto.startswith('```json'):
        respuesta_texto = respuesta_texto[7:-3]
    elif respuesta_texto.startswith('```'):
        respuesta_texto = respuesta_texto[3:-3]

    codigo = json.loads(respuesta_texto.strip())
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html", ""))
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Código generado y archivos guardados con éxito con efecto Parallax!")

except Exception as e:
    print(f"Error al generar la web: {e}")
    print("Nota: Si el error menciona '503 UNAVAILABLE', los servidores están muy ocupados en este momento. Solo tienes que esperar unos minutos y volver a darle a 'Run workflow'.")
