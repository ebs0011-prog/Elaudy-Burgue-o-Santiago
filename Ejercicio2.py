# 1️⃣ Importar librerías necesarias
import requests                 # Para hacer peticiones HTTP
from bs4 import BeautifulSoup   # Para parsear HTML
import re                       # Para expresiones regulares
import sqlite3                  # Para trabajar con bases de datos SQLite

# 2️⃣ Hacer la petición HTTP al medio de noticias
url = "https://as.com/"        # URL del sitio
respuesta = requests.get(url)  # Hacemos la petición GET
print(respuesta.status_code)   # Imprime 200 si todo va bien
#print(respuesta.text[:500])   # Opcional: ver los primeros 500 caracteres del HTML

# 3️⃣ Parsear el HTML con BeautifulSoup
soup = BeautifulSoup(respuesta.text, "html.parser")
print(soup.title)              # Título del sitio
print(soup.title.text)         # Texto del título

# 4️⃣ Buscar titulares (h2) y limitar a 10
titulares = soup.find_all("h2")
for t in titulares[:10]:
    print(t.text.strip())      # Limpiamos espacios

# 5️⃣ Guardar titulares en un archivo HTML (opcional)
with open("titulares.html", "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n")
    f.write("    <meta charset='UTF-8'>\n")
    f.write("    <title>Titulares</title>\n")
    f.write("</head>\n<body>\n")
    f.write("    <h1>Últimos titulares</h1>\n<ol>\n")
    for t in titulares[:10]:
        f.write(f"        <li>{t.text.strip()}</li>\n")
    f.write("    </ol>\n</body>\n</html>\n")

# 6️⃣ Preparar la base de datos SQLite
conn = sqlite3.connect("noticias.db")  # Crear o abrir la base de datos
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS noticias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    enlace TEXT,
    fecha TEXT,
    autor TEXT
)
""")
conn.commit()  # Guardar cambios

# 7️⃣ Extraer datos de cada titular y guardarlos en la base de datos
noticias = []  # Lista temporal
for t in titulares[:10]:
    titulo = t.text.strip()[:150]                  # Limitar a 150 caracteres
    enlace = t.find("a")["href"] if t.find("a") else ""
    fecha_match = re.search(r"\d{2}/\d{2}/\d{4}|\d{4}", t.text)  # Buscar fechas dd/mm/aaaa o año
    fecha = fecha_match.group(0) if fecha_match else "Sin fecha"
    autor = "Autor/Sección"  # Como ejemplo, puedes mejorar luego

    noticias.append((titulo, enlace, fecha, autor))

    # Insertar en la base de datos
    cursor.execute("""
    INSERT INTO noticias (titulo, enlace, fecha, autor)
    VALUES (?, ?, ?, ?)
    """, (titulo, enlace, fecha, autor))

conn.commit()  # Guardar cambios
conn.close()   

print("Noticias guardadas en base de datos")
