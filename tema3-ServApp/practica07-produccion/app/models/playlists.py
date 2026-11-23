from contextlib import closing, contextmanager

from .canciones import conectar_bd


@contextmanager
def transaccion_playlist(usuario_id, playlist_id):
    with closing(conectar_bd()) as conexion:
        try:
            with conexion.cursor() as cursor:
                # Serializa los cambios de una misma playlist y comprueba su dueño.
                cursor.execute(
                    "SELECT id FROM playlists WHERE id = %s AND usuario_id = %s FOR UPDATE",
                    (playlist_id, usuario_id)
                )
                yield cursor if cursor.fetchone() else None
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise


def listar_playlists(usuario_id):
    with closing(conectar_bd()) as conexion, conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.id, p.nombre, p.descripcion, COUNT(DISTINCT pc.cancion_id) AS total
            FROM playlists AS p
            LEFT JOIN playlist_canciones AS pc ON pc.playlist_id = p.id
            WHERE p.usuario_id = %s
            GROUP BY p.id, p.nombre, p.descripcion
            ORDER BY p.nombre, p.id
            """,
            (usuario_id,)
        )
        return cursor.fetchall()


def consultar_playlist(usuario_id, playlist_id):
    with closing(conectar_bd()) as conexion, conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.id, p.nombre, p.descripcion, c.id AS cancion_id,
                   c.titulo, c.artista, c.album, c.genero, c.imagen_url, c.spotify_url
            FROM playlists AS p
            LEFT JOIN playlist_canciones AS pc ON pc.playlist_id = p.id
            LEFT JOIN canciones AS c ON c.id = pc.cancion_id
            WHERE p.id = %s AND p.usuario_id = %s
            ORDER BY c.artista, c.titulo, c.id
            """,
            (playlist_id, usuario_id)
        )
        filas = cursor.fetchall()

    if not filas:
        return None, []

    playlist = {campo: filas[0][campo] for campo in ("id", "nombre", "descripcion")}
    canciones = {}
    for fila in filas:
        cancion_id = fila.pop("cancion_id")
        if cancion_id is not None:
            canciones[cancion_id] = dict(fila, id=cancion_id)
    return playlist, list(canciones.values())


def crear_playlist(usuario_id, nombre, descripcion):
    with closing(conectar_bd()) as conexion, conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO playlists (usuario_id, nombre, descripcion) VALUES (%s, %s, %s)",
            (usuario_id, nombre, descripcion)
        )
        playlist_id = cursor.lastrowid
        conexion.commit()
        return playlist_id


def editar_playlist(usuario_id, playlist_id, nombre, descripcion):
    with transaccion_playlist(usuario_id, playlist_id) as cursor:
        if cursor is None:
            return False
        cursor.execute(
            "UPDATE playlists SET nombre = %s, descripcion = %s WHERE id = %s",
            (nombre, descripcion, playlist_id)
        )
        return True


def eliminar_playlist(usuario_id, playlist_id):
    with transaccion_playlist(usuario_id, playlist_id) as cursor:
        if cursor is None:
            return False
        cursor.execute("DELETE FROM playlist_canciones WHERE playlist_id = %s", (playlist_id,))
        cursor.execute("DELETE FROM playlists WHERE id = %s", (playlist_id,))
        return True


def agregar_cancion(usuario_id, playlist_id, cancion_id):
    with transaccion_playlist(usuario_id, playlist_id) as cursor:
        if cursor is None:
            return False
        cursor.execute("SELECT id FROM canciones WHERE id = %s", (cancion_id,))
        if cursor.fetchone() is None:
            return False
        cursor.execute(
            """
            INSERT INTO playlist_canciones (playlist_id, cancion_id)
            SELECT %s, %s FROM DUAL
            WHERE NOT EXISTS (
                SELECT 1 FROM playlist_canciones WHERE playlist_id = %s AND cancion_id = %s
            )
            """,
            (playlist_id, cancion_id, playlist_id, cancion_id)
        )
        return True


def quitar_cancion(usuario_id, playlist_id, cancion_id):
    with transaccion_playlist(usuario_id, playlist_id) as cursor:
        if cursor is None:
            return False
        cursor.execute(
            "DELETE FROM playlist_canciones WHERE playlist_id = %s AND cancion_id = %s",
            (playlist_id, cancion_id)
        )
        return True
