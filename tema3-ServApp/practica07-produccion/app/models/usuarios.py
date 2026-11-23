from models.canciones import conectar_bd


def guardar_usuario_google(google_id, nombre, email, avatar_url):
    conexion = conectar_bd()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO usuarios (google_id, nombre, email, avatar_url)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    google_id = VALUES(google_id),
                    nombre = VALUES(nombre),
                    avatar_url = VALUES(avatar_url)
            """, (google_id, nombre, email, avatar_url))
            cursor.execute("""
                SELECT id, google_id, nombre, email, avatar_url
                FROM usuarios WHERE google_id = %s
            """, (google_id,))
            usuario = cursor.fetchone()
        conexion.commit()
        return usuario
    finally:
        conexion.close()
