import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- AQUÍ PONES TU PROMPT DEL MILLÓN ---
prompt = """
Eres un desarrollador web experto. Crea el código HTML, CSS y JavaScript en un solo archivo 
para una página web. 
El tema de la página es: Somos una empresa de IIOT (Industrial Internet of Things) que hemos generado un nueo programa para el manenimiento y el OEE de las maquinas. 
Somos unos desarrolladores a pie de planta. Quiero que me hagas una pagina futurista, similar a la pagina "Baliatekks", pero el color que nosotros tenemos como principal es el azul oscuro
IMPORTANTE: Devuelve ÚNICAMENTE el código HTML crudo. No incluyas explicaciones, 
ni formato markdown (no uses ```html). Solo empieza con <!DOCTYPE html> y termina con </html>.
"""
# ---------------------------------------

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

# Obtenemos la respuesta de la IA
codigo_html = response.text.strip()

# Pequeño truco de seguridad por si la IA añade las comillas de código (```html) por error
if codigo_html.startswith("```html"):
    codigo_html = codigo_html[7:-3]
elif codigo_html.startswith("```"):
    codigo_html = codigo_html[3:-3]

# Guardamos TODO el código nuevo reemplazando el viejo index.html
with open("index.html", "w", encoding="utf-8") as file:
    file.write(codigo_html.strip())
    
print("¡Archivo index.html reconstruido desde cero con éxito!")
