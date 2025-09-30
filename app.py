from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # Obtener parámetros del formulario de búsqueda/filtro
    buscar = request.args.get("buscar", "")
    autor = request.args.get("autor", "")

    # Conectar a la base de datos
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()

    # Consulta principal con búsqueda y filtro
    query = "SELECT titulo, enlace, fecha, autor FROM noticias WHERE 1=1"
    params = []

    if buscar:
        query += " AND titulo LIKE ?"
        params.append(f"%{buscar}%")
    if autor:
        query += " AND autor = ?"
        params.append(autor)

    cursor.execute(query, params)
    noticias = cursor.fetchall()

    # Consultar autores únicos para el filtro
    cursor.execute("SELECT DISTINCT autor FROM noticias")
    autores = [a[0] for a in cursor.fetchall()]

    conn.close()

    return render_template("index.html", noticias=noticias, buscar=buscar, autor=autor, autores=autores)

if __name__ == "__main__":
    app.run(debug=True)
