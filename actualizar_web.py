import os
from google import genai

# 1. Configurar el cliente usando el secreto de GitHub y la nueva librería
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 2. Pedirle a la IA que genere contenido
prompt = "Escribe un breve dato curioso sobre la historia de la tecnología en una sola línea, sin comillas."
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)
dato_curioso = response.text.strip()

# 3. Crear el nuevo código HTML con el dato incrustado
html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Web Automática</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
        h1 {{ color: #333; }}
        p {{ color: #555; font-size: 1.2em; }}
    </style>
</head>
<body>
    <h1>Dato Curioso del Día 🤖</h1>
    <p>{dato_curioso}</p>
</body>
</html>"""

# 4. Guardar y sobrescribir el archivo index.html
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
    
print("¡Archivo index.html actualizado con éxito!")
