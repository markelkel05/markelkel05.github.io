import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- PASO 1: CREAR CARPETAS ---
os.makedirs("css", exist_ok=True)
os.makedirs("js", exist_ok=True)
os.makedirs("img", exist_ok=True) # Nueva carpeta para nuestras imágenes

# --- PASO 2: GENERAR IMAGEN CON IA ---
print("Generando imagen futurista de IIOT...")
try:
    resultado_img = client.models.generate_images(
        model='imagen-3.0-generate-001',
        prompt='Una fábrica industrial moderna e inteligente por dentro, hiperrealista, estilo futurista, tecnología IIOT, iluminación cinematográfica, color predominante azul oscuro',
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="16:9",
            output_mime_type="image/jpeg"
        )
    )
    
    # Guardamos la imagen generada en la carpeta img
    with open("img/fondo1.jpg", "wb") as f:
        f.write(resultado_img.generated_images[0].image.image_bytes)
    print("¡Imagen generada y guardada como fondo1.jpg!")
    
except Exception as e:
    print(f"Error al generar la imagen: {e}")
    print("Asegúrate de que tu clave de API tiene acceso a la generación de imágenes.")

# --- PASO 3: GENERAR LA WEB CON GEMINI ---
print("Generando el código de la web...")
prompt = """
Eres un desarrollador web experto. Crea una página web para una empresa de IIOT (Industrial Internet of Things) que ha generado un nuevo programa para el mantenimiento y el OEE de las máquinas. 
Somos desarrolladores a pie de planta. El diseño debe ser futurista, similar a "Baliatekks", con azul oscuro como color principal.

IMPORTANTE: 
1. Divide el código en HTML, CSS y JavaScript.
2. El HTML DEBE estar enlazado a las carpetas correctas: <link rel="stylesheet" href="css/style.css"> y <script src="js/script.js"></script>.
3. REQUISITO PARALLAX: Incluye una sección con Efecto Parallax amplio. Para la imagen de fondo de esta sección, DEBES usar estrictamente la ruta local: img/fondo1.jpg
4. Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, sin comillas Markdown:
{
  "html": "código html aquí",
  "css": "código css aquí",
  "js": "código javascript aquí"
}
"""

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

respuesta_texto = response.text.strip()

# Limpieza de seguridad
if respuesta_texto.startswith('```json'):
    respuesta_texto = respuesta_texto[7:-3]
elif respuesta_texto.startswith('
```'):
    respuesta_texto = respuesta_texto[3:-3]

try:
    codigo = json.loads(respuesta_texto.strip())
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(codigo.get("html", ""))
        
    with open("css/style.css", "w", encoding="utf-8") as f:
        f.write(codigo.get("css", ""))
        
    with open("js/script.js", "w", encoding="utf-8") as f:
        f.write(codigo.get("js", ""))
        
    print("¡Código generado y archivos guardados con éxito!")

except json.JSONDecodeError:
    print("Error: La IA no devolvió un formato JSON válido.")
