import csv
from contextlib import closing
from pathlib import Path
from urllib.parse import quote

from models.canciones import conectar_bd


PORTADAS = {
    "Electronic": "electronica", "Trip-hop": "electronica",
    "Indie rock": "rock", "Rock": "rock", "Alternative": "rock", "Rock latino": "rock",
    "R&B": "soul", "Hip-hop": "soul", "Urbano latino": "soul",
    "Pop español": "pop", "Pop latino": "pop", "Jazz": "jazz",
}


def migrar():
    with closing(conectar_bd()) as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT GET_LOCK('soundwave.catalogo.v1', 15) AS adquirido")
        if cursor.fetchone()["adquirido"] != 1:
            raise RuntimeError("No se pudo bloquear la migración del catálogo.")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dj_cuotas (
                dia DATE NOT NULL,
                titular INT NOT NULL,
                consultas SMALLINT UNSIGNED NOT NULL,
                PRIMARY KEY (dia, titular)
            ) ENGINE=InnoDB
        """)
        with Path(__file__).with_name("catalogo.tsv").open(encoding="utf-8") as archivo:
            for titulo, artista, album, genero in csv.reader(archivo, delimiter="|"):
                portada = f"/static/img/generos/{PORTADAS[genero]}.png"
                busqueda = quote(f"{titulo} {artista}", safe="")
                cursor.execute("""
                    INSERT INTO canciones (titulo, artista, album, genero, imagen_url, spotify_url)
                    SELECT %s, %s, %s, %s, %s, %s FROM DUAL
                    WHERE NOT EXISTS (
                        SELECT 1 FROM canciones WHERE titulo = %s AND artista = %s
                    )
                """, (titulo, artista, album, genero, portada,
                      f"https://open.spotify.com/search/{busqueda}", titulo, artista))
        conexion.commit()
        # MariaDB libera el bloqueo al cerrar la conexión, también si falla la migración.


if __name__ == "__main__":
    migrar()
