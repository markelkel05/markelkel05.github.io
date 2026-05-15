import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PROMPT ACTUALIZADO ---
prompt = """
Eres un desarrollador web experto. Crea una página web para una empresa de IIOT (Industrial Internet of Things). 
El diseño debe ser futurista, similar a "Baliatekks", con azul oscuro como color principal.

IMPORTANTE: 
1. Divide el código en HTML, CSS y JavaScript.
2. El HTML DEBE estar enlazado a las carpetas correctas: usa <link rel="stylesheet" href="css/style.css"> en el <head> y <script src="js/script.js"></script> justo antes de cerrar el <body>.
3. Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, sin comillas Markdown:
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

# Limpieza de seguridad
if respuesta_texto.startswith("```json"):
    respuesta_texto = respuesta_texto[7:-3]
elif respuesta_texto.startswith("
```"):
    respuesta_texto = respuesta_texto[3:-3]

respuesta_texto = respuesta_texto.strip()

try:
    codigo = json.loads(respuesta_texto)
    
    # --- LA MAGIA DE LAS CARPETAS ESTÁ AQUÍ ---
    # Python crea las carpetas si no existen (exist_ok=True evita errores si ya están creadas)
    os.makedirs("css", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    
    # Guardamos los archivos dentro de sus respectivas carpetas
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html", ""))
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Archivos y carpetas creados con éxito!")

except json.JSONDecodeError:
    print("Error: La IA no devolvió un formato JSON válido.")
