
import os
import pymysql
from flask import Flask, render_template_string

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mariadb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")
DB_NAME = os.getenv("DB_NAME", "practica05javier")


HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Práctica 05 - Lista de tareas</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            padding: 30px;
        }
        h1 { color: #333; }
        table {
            border-collapse: collapse;
            width: 100%;
            background: white;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th { background: #333; color: white; }
    </style>
</head>
<body>
    <h1>Mis tareas - Práctica 05</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Descripción</th>
            <th>Completada</th>
        </tr>
        {% for tarea in tareas %}
        <tr>
            <td>{{ tarea.id }}</td>
            <td>{{ tarea.titulo }}</td>
            <td>{{ tarea.descripcion }}</td>
            <td>{{ "Sí" if tarea.completada else "No" }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route("/")
def inicio():
    try:
        conexion = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )

        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tareas")
            tareas = cursor.fetchall()

        conexion.close()

        return render_template_string(HTML, tareas=tareas)

    except Exception as error:
        return f"Error al conectar con MariaDB: {error}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
