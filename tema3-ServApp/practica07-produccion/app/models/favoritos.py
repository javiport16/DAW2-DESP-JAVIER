from models.canciones import conectar_bd


def obtener_favoritos(usuario_id):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.titulo, c.artista, c.album,
                       c.genero, c.imagen_url, c.spotify_url
                FROM favoritos f
                JOIN canciones c ON c.id = f.cancion_id
                WHERE f.usuario_id = %s
                ORDER BY c.artista, c.titulo
            """, (usuario_id,))
            return cursor.fetchall()
    finally:
        conexion.close()


def agregar_favorito(usuario_id, cancion_id):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT IGNORE INTO favoritos (usuario_id, cancion_id) VALUES (%s, %s)",
                (usuario_id, cancion_id)
            )
        conexion.commit()
    finally:
        conexion.close()


def eliminar_favorito(usuario_id, cancion_id):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM favoritos WHERE usuario_id = %s AND cancion_id = %s",
                (usuario_id, cancion_id)
            )
        conexion.commit()
    finally:
        conexion.close()
