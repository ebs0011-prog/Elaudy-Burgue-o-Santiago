import requests
from bs4 import BeautifulSoup
import re  # <- esto faltaba

url = "https://as.com/"
respuesta = requests.get(url)

print(respuesta.status_code)
print(respuesta.text[:500])

soup = BeautifulSoup(respuesta.text, "html.parser")

print(soup.title)
print(soup.title.text)

titulares = soup.find_all("h2")

for t in titulares[:10]:
    print(t.text.strip())

# Guardar titulares en un archivo HTML
with open("titulares.html", "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html lang='es'>\n")
    f.write("<head>\n")
    f.write("    <meta charset='UTF-8'>\n")
    f.write("    <title>Titulares</title>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("    <h1>Últimos titulares</h1>\n")
    f.write("    <ol>\n")  # <- abrimos la lista

    for t in titulares[:10]:
        f.write(f"        <li>{t.text.strip()}</li>\n")

    f.write("    </ol>\n")  # <- cerramos la lista
    f.write("</body>\n")
    f.write("</html>\n")

# Crear lista de noticias con título, enlace, fecha y autor/sección
noticias = []

for t in titulares[:10]:
    titulo = t.text.strip()[:150]   # limitar a 150 caracteres
    enlace = t.find("a")["href"] if t.find("a") else ""
    fecha = re.search(r"\d{4}", t.text)  # buscar año en el titular
    fecha = fecha.group(0) if fecha else "Sin fecha"
    
    noticias.append((titulo, enlace, fecha, "Autor/Sección"))

print(noticias)  # <- para ver cómo quedó la lista
