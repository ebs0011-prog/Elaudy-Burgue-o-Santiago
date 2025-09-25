import requests

url = "https://as.com/"
respuesta = requests.get(url)

print(respuesta.status_code)
print(respuesta.text[:500])

from bs4 import BeautifulSoup

soup = BeautifulSoup(respuesta.text, "html.parser")

print(soup.title)
print(soup.title.text)

titulares = soup.find_all("h2")

for t in titulares[:5]:
    print(t.text.strip())

#esto es un corte 

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

    for t in titulares [:5]:
        f.write(f"        <li>{t.text.strip()}</li>\n")
        f.write("    </ol>\n")  


    f.write("</body>\n")
    f.write("</html>\n")
