# Importar librerías
import requests
from bs4 import BeautifulSoup
import sqlite3
import re


url = "https://elpais.com/"
respuesta = requests.get(url)
print("Estado:", respuesta.status_code)

soup = BeautifulSoup(respuesta.text, "html.parser")

# Buscar titulares principales (h2)
titulares = soup.find_all("h2")[:10]  # limitamos a 10 titulares
print("Titulares encontrados:", len(titulares))

#  Conectar a SQLite
conn = sqlite3.connect("noticias.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS noticias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    enlace TEXT,
    fecha TEXT,
    autor TEXT
)
""")
conn.commit()

# Procesar titulares y guardar en la BD
for t in titulares:
    titulo = t.get_text(strip=True)[:150]   # Limitar texto
    enlace = t.find("a")["href"] if t.find("a") else ""

    # Buscar fecha del texto
    fecha_match = re.search(r"\d{2}/\d{2}/\d{4}|\d{4}", t.text)
    fecha = fecha_match.group(0) if fecha_match else "Sin fecha"

    
    autor = "El País"  

    cursor.execute("""
    INSERT INTO noticias (titulo, enlace, fecha, autor)
    VALUES (?, ?, ?, ?)
    """, (titulo, enlace, fecha, autor))

conn.commit()
conn.close()

print("Noticias guardadas en noticias.db")

