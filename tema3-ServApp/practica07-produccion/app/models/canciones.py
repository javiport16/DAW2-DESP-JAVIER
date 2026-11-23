import os
import pymysql
from pymysql.cursors import DictCursor


def conectar_bd():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "mariadb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "soundwave_db"),
        cursorclass=DictCursor,
        charset="utf8mb4"
    )


def obtener_canciones(busqueda="", genero=""):
    conexion = conectar_bd()

    try:
        sql = """
            SELECT id, titulo, artista, album, genero,
                   imagen_url, spotify_url
            FROM canciones
            WHERE (titulo LIKE %s OR artista LIKE %s)
        """
        patron = f"%{busqueda}%"
        parametros = [patron, patron]

        if genero:
            sql += " AND genero = %s"
            parametros.append(genero)

        sql += " ORDER BY artista, titulo"

        with conexion.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
    finally:
        conexion.close()


def obtener_generos():
    conexion = conectar_bd()

    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT genero FROM canciones "
                "WHERE genero IS NOT NULL ORDER BY genero"
            )
            return [fila["genero"] for fila in cursor.fetchall()]
    finally:
        conexion.close()