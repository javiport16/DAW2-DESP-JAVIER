
from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route("/")
def inicio():
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Práctica Proxy Inverso SSL</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #eef2f7;
                margin: 0;
                padding: 40px 16px;
            }}
            main {{
                max-width: 650px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 14px;
                box-shadow: 0 4px 18px #0001;
            }}
            h1 {{ color: #1769aa; }}
        </style>
    </head>
    <body>
        <main>
            <h1>Práctica de Proxy Inverso Nginx</h1>
            <p><strong>Alumno:</strong> TU NOMBRE Y APELLIDOS</p>
            <p><strong>Centro:</strong> TU CENTRO</p>
            <p><strong>Ciclo:</strong> CFGS DAW</p>
            <p><strong>Grupo:</strong> TU GRUPO</p>
            <p><strong>Fecha de despliegue:</strong> {date.today()}</p>
            <p>Aplicación Flask funcionando correctamente.</p>
            <p>Acceso protegido mediante Nginx y HTTPS.</p>
        </main>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
