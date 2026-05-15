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
Eres un desarrollador web experto. Crea una página web para una empresa de IIOT (Industrial Internet of Things) que ha generado un nuevo programa para el mantenimiento y el OEE de las máquinas. 
Somos desarrolladores a pie de planta. El diseño debe ser futurista, similar (casi igual) a "www.Baliatekks.com", con azul oscuro como color principal.

Por ahora la estructura esta bien, pero queiro que repitas el estilo de la imagen del titulo (El que tiene el efecto Parallax) y en donde hay espacios en negro, lo repitas, en este caso,
los archivos se llaman "IIOT_2.jpeg" y "IIOT_3.jpeg", agregalos con <img src="*aqui van el nombre de uno de los archivos*">. tambien en el menu aparece Kentu.IIOT, quitale el ".IIOT"

IMPORTANTE: 
1. Divide el código en HTML, CSS y JavaScript.
2. El HTML DEBE estar enlazado a las carpetas correctas: <link rel="stylesheet" href="css/style.css"> y <script src="js/script.js"></script>.
3. REQUISITO PARALLAX: Incluye secciones con Efecto Parallax amplio (background-attachment: fixed). Usa imágenes gratuitas de Unsplash para los fondos fijos (ejemplo: https://source.unsplash.com/random/1920x1080/?industry,factory,technology).
4. Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, sin comillas Markdown:
{
  "html": "código html aquí",
  "css": "código css aquí",
  "js": "código javascript aquí"
}
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
