import sqlite3
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

BASE_DATOS = "usuarios.db"


def crear_base_datos():
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    usuarios = [
        ("fabian", "claveFabian123"),
        ("felipe", "claveFelipe123")
    ]

    for usuario, password in usuarios:
        password_hash = generate_password_hash(password)

        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (usuario, password_hash)
            VALUES (?, ?)
        """, (usuario, password_hash))

    conexion.commit()
    conexion.close()


def validar_usuario(usuario, password):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT password_hash FROM usuarios
        WHERE usuario = ?
    """, (usuario,))

    resultado = cursor.fetchone()
    conexion.close()

    if resultado is None:
        return False

    password_hash = resultado[0]

    return check_password_hash(password_hash, password)


@app.route("/")
def inicio():
    return """
    <html>
        <head>
            <title>Gestión de Usuarios</title>
        </head>
        <body>
            <h1>Validación de Usuarios</h1>

            <form action="/login" method="post">
                <label>Usuario:</label>
                <input type="text" name="usuario" required><br><br>

                <label>Contraseña:</label>
                <input type="password" name="password" required><br><br>

                <button type="submit">Ingresar</button>
            </form>
        </body>
    </html>
    """


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"].lower()
    password = request.form["password"]

    if validar_usuario(usuario, password):
        return f"""
        <h1>Acceso permitido</h1>
        <p>Bienvenido, {usuario}</p>
        <a href="/">Volver</a>
        """
    else:
        return """
        <h1>Acceso denegado</h1>
        <p>Usuario o contraseña incorrectos.</p>
        <a href="/">Volver</a>
        """


if __name__ == "__main__":
    crear_base_datos()
    app.run(host="0.0.0.0", port=5800)
