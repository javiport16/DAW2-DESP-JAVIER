CREATE DATABASE IF NOT EXISTS soundwave_db;
USE soundwave_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    google_id VARCHAR(255) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    avatar_url TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS canciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    artista VARCHAR(200) NOT NULL,
    album VARCHAR(200),
    genero VARCHAR(100),
    imagen_url TEXT,
    spotify_url TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS playlist_canciones (
    playlist_id INT NOT NULL,
    cancion_id INT NOT NULL,
    PRIMARY KEY (playlist_id, cancion_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(id)
        ON DELETE CASCADE,
    FOREIGN KEY (cancion_id) REFERENCES canciones(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS favoritos (
    usuario_id INT NOT NULL,
    cancion_id INT NOT NULL,
    PRIMARY KEY (usuario_id, cancion_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    FOREIGN KEY (cancion_id) REFERENCES canciones(id)
        ON DELETE CASCADE
);