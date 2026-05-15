import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- AQUÍ PONES TU PROMPT DEL MILLÓN ---
prompt = """
Eres un desarrollador web experto. Crea una página web para una empresa de IIOT (Industrial Internet of Things) que ha generado un nuevo programa para el mantenimiento y el OEE de las máquinas. 
Somos desarrolladores a pie de planta. El diseño debe ser futurista, similar a "Baliatekks", con azul oscuro como color principal.

IMPORTANTE: 
1. Divide el código en tres partes: HTML, CSS y JavaScript.
2. El HTML DEBE incluir <link rel="stylesheet" href="style.css"> en el <head> y <script src="script.js"></script> justo antes de cerrar el <body>.
3. Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, sin comillas Markdown ni texto extra:
{
  "html": "código html aquí",
  "css": "código css aquí",
  "js": "código javascript aquí"
}
"""
# ---------------------------------------

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

respuesta_texto = response.text.strip()

# Limpieza de seguridad por si la IA añade las etiquetas Markdown (```json)
if respuesta_texto.startswith("```json"):
    respuesta_texto = respuesta_texto[7:-3]
elif respuesta_texto.startswith("```"):
    respuesta_texto = respuesta_texto[3:-3]

respuesta_texto = respuesta_texto.strip()

try:
    # Convertimos el texto de la IA en un diccionario de Python
    codigo = json.loads(respuesta_texto)
    
    # 1. Guardar HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html", ""))
        
    # 2. Guardar CSS
    with open("style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    # 3. Guardar JavaScript
    with open("script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Archivos index.html, style.css y script.js creados y separados con éxito!")

except json.JSONDecodeError:
    print("Error: La IA no devolvió un formato JSON válido.")
    print("Respuesta cruda:", respuesta_texto)
