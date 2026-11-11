from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <html>
        <head>
            <title>Práctica 3 - Flask</title>
        </head>
        <body>
            <h1>¡Bienvenido a mi aplicación Flask!</h1>
            <h2>Alumno: Javier</h2>
            <p>Práctica 3: Despliegue de Flask con Gunicorn y Nginx.</p>
            <p>Aplicación desarrollada con Python y Flask.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run()