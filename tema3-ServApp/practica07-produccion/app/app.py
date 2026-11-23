import os
from functools import wraps

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, abort
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client import OAuthError
from flask.sessions import SecureCookieSessionInterface
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from models.canciones import obtener_canciones, obtener_generos
from models.usuarios import guardar_usuario_google
from models.favoritos import (
    obtener_favoritos,
    agregar_favorito,
    eliminar_favorito
)
from models.playlists import (
    agregar_cancion, consultar_playlist, crear_playlist, editar_playlist,
    eliminar_playlist, listar_playlists, quitar_cancion
)


from dj import dj
from portadas import portada_catalogo


class SesionPorProtocolo(SecureCookieSessionInterface):
    def get_cookie_secure(self, app):
        return request.is_secure


app = Flask(__name__)
app.session_interface = SesionPorProtocolo()
app.register_blueprint(dj)
app.jinja_env.globals["portada_catalogo"] = portada_catalogo

app.secret_key = os.environ["FLASK_SECRET_KEY"]
csrf = CSRFProtect(app)

# Permite que Flask reconozca HTTPS detrás de Nginx Proxy Manager.
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1
)

app.config.update(
    TRUSTED_HOSTS=["localhost", "127.0.0.1", "javierportela1.piodaw.site"],
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

# Configuración de Google OAuth
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url=(
        "https://accounts.google.com/.well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email profile"
    }
)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/explorar")
def explorar():
    busqueda = request.args.get("q", "").strip()
    genero = request.args.get("genero", "").strip()

    canciones = obtener_canciones(busqueda, genero)
    generos = obtener_generos()

    return render_template(
        "explorar.html",
        canciones=canciones,
        generos=generos,
        busqueda=busqueda,
        genero_actual=genero
    )


@app.route("/api/canciones")
def api_canciones():
    busqueda = request.args.get("q", "").strip()
    canciones = obtener_canciones(busqueda)
    return jsonify(canciones)


@app.route("/login")
def login():
    dominio = request.host.split(":", 1)[0]
    if dominio == "127.0.0.1":
        return redirect("http://localhost:8005/login")
    if dominio == "javierportela1.piodaw.site":
        redirect_uri = "https://javierportela1.piodaw.site/auth/callback"
    else:
        redirect_uri = "http://localhost:8005/auth/callback"

    return google.authorize_redirect(redirect_uri)


@app.route("/auth/callback")
def auth_callback():
    try:
        token = google.authorize_access_token()
    except OAuthError:
        return "No se pudo completar el inicio de sesión con Google. Vuelve a intentarlo.", 400
    perfil = token.get("userinfo")

    if not perfil:
        return "No se pudo obtener el perfil de Google", 400

    if not perfil.get("email_verified"):
        return "Google no ha verificado este correo", 403

    usuario = guardar_usuario_google(
        google_id=perfil["sub"],
        nombre=perfil.get("name", "Usuario"),
        email=perfil["email"],
        avatar_url=perfil.get("picture", "")
    )

    if not usuario:
        return "No se pudo guardar el usuario", 500

    session.clear()
    session["usuario_id"] = usuario["id"]
    session["nombre"] = usuario["nombre"]
    session["avatar_url"] = usuario["avatar_url"]

    return redirect(url_for("inicio"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("inicio"))


@app.route("/biblioteca")
def biblioteca():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    canciones = obtener_favoritos(session["usuario_id"])

    return render_template(
        "biblioteca.html",
        canciones=canciones
    )


@app.route("/favoritos/<int:cancion_id>/agregar", methods=["POST"])
def guardar_favorito(cancion_id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    agregar_favorito(session["usuario_id"], cancion_id)
    return redirect(url_for("explorar"))


@app.route("/favoritos/<int:cancion_id>/eliminar", methods=["POST"])
def borrar_favorito(cancion_id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    eliminar_favorito(session["usuario_id"], cancion_id)
    return redirect(url_for("biblioteca"))


def sesion_playlist(recurso):
    @wraps(recurso)
    def vista(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return recurso(session["usuario_id"], *args, **kwargs)
    return vista


def datos_playlist():
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    if not nombre or len(nombre) > 100 or len(descripcion) > 255:
        abort(400, description="Introduce un nombre de 1 a 100 caracteres y una descripción de hasta 255.")
    return nombre, descripcion


@app.route("/playlists", methods=["GET", "POST"])
@sesion_playlist
def playlists(usuario_id):
    if request.method == "POST":
        playlist_id = crear_playlist(usuario_id, *datos_playlist())
        return redirect(url_for("detalle_playlist", playlist_id=playlist_id), code=303)

    return render_template("playlists.html", playlists=listar_playlists(usuario_id))


@app.route("/playlists/<int:playlist_id>")
@sesion_playlist
def detalle_playlist(usuario_id, playlist_id):
    playlist, canciones = consultar_playlist(usuario_id, playlist_id)
    if playlist is None:
        abort(404)

    busqueda = request.args.get("q", "").strip()
    ids_guardados = {cancion["id"] for cancion in canciones}
    disponibles = [
        cancion for cancion in obtener_canciones(busqueda)
        if cancion["id"] not in ids_guardados
    ]
    return render_template(
        "playlist_detalle.html",
        playlist=playlist,
        canciones=canciones,
        disponibles=disponibles,
        busqueda=busqueda
    )


@app.route("/playlists/<int:playlist_id>/editar", methods=["POST"])
@sesion_playlist
def actualizar_playlist(usuario_id, playlist_id):
    if not editar_playlist(usuario_id, playlist_id, *datos_playlist()):
        abort(404)
    return redirect(url_for("detalle_playlist", playlist_id=playlist_id), code=303)


@app.route("/playlists/<int:playlist_id>/eliminar", methods=["POST"])
@sesion_playlist
def borrar_playlist(usuario_id, playlist_id):
    if not eliminar_playlist(usuario_id, playlist_id):
        abort(404)
    return redirect(url_for("playlists"), code=303)


@app.route("/playlists/<int:playlist_id>/canciones", methods=["POST"])
@sesion_playlist
def guardar_cancion_playlist(usuario_id, playlist_id):
    cancion_id = request.form.get("cancion_id", type=int)
    if cancion_id is None or not 0 < cancion_id <= 2**31 - 1:
        abort(400, description="Selecciona una canción del catálogo.")
    if not agregar_cancion(usuario_id, playlist_id, cancion_id):
        abort(404)
    return redirect(url_for("detalle_playlist", playlist_id=playlist_id), code=303)


@app.route("/playlists/<int:playlist_id>/canciones/<int:cancion_id>/eliminar", methods=["POST"])
@sesion_playlist
def borrar_cancion_playlist(usuario_id, playlist_id, cancion_id):
    if not quitar_cancion(usuario_id, playlist_id, cancion_id):
        abort(404)
    return redirect(url_for("detalle_playlist", playlist_id=playlist_id), code=303)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
