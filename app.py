"""
SmartDispatch - Sistema de Login y Registro (Cliente / Soporte)
Servidor Web Flask con autenticación segura en base de datos SQLite.
"""

import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import database

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "smartdispatch_login_secret_key_2026")

# Asegurar que la base de datos esté inicializada
database.init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Por favor inicia sesión para continuar.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Por favor completa todos los campos.", "danger")
            return render_template("login.html")

        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.nombre, u.email, u.password_hash, u.empresa, u.estado, r.nombre AS rol
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id
            WHERE u.email = ?
        """, (email,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            flash("Correo electrónico no encontrado.", "danger")
            return render_template("login.html")

        if user["estado"] != "activo":
            conn.close()
            flash("Esta cuenta se encuentra inactiva o bloqueada.", "danger")
            return render_template("login.html")

        if not check_password_hash(user["password_hash"], password):
            conn.close()
            flash("Contraseña incorrecta.", "danger")
            return render_template("login.html")

        # Registrar en auditoría de accesos
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ua = request.headers.get("User-Agent", "Desconocido")
        cursor.execute("""
            INSERT INTO historial_accesos (usuario_id, ip_origen, user_agent)
            VALUES (?, ?, ?)
        """, (user["id"], ip, ua))
        conn.commit()
        conn.close()

        # Guardar en sesión
        session.clear()
        session["user_id"] = user["id"]
        session["nombre"] = user["nombre"]
        session["email"] = user["email"]
        session["empresa"] = user["empresa"]
        session["rol"] = user["rol"]

        flash(f"¡Bienvenido(a), {user['nombre']}!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registro de nuevos usuarios (Clientes o Personal de Soporte)."""
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        rol = request.form.get("rol", "cliente").strip()
        empresa = request.form.get("empresa", "").strip()
        telefono = request.form.get("telefono", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not nombre or not email or not password:
            flash("Nombre, correo y contraseña son obligatorios.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "warning")
            return render_template("register.html")

        conn = database.get_db()
        cursor = conn.cursor()

        # Verificar si email ya existe
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            flash("Este correo electrónico ya está registrado. Por favor inicia sesión.", "warning")
            return redirect(url_for("login"))

        # Obtener rol_id correspondiente
        cursor.execute("SELECT id FROM roles WHERE nombre = ?", (rol,))
        rol_row = cursor.fetchone()
        if not rol_row:
            cursor.execute("SELECT id FROM roles WHERE nombre = 'cliente'")
            rol_row = cursor.fetchone()
        rol_id = rol_row["id"]

        p_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO usuarios (rol_id, nombre, email, password_hash, telefono, empresa)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (rol_id, nombre, email, p_hash, telefono, empresa))
        conn.commit()
        conn.close()

        flash("¡Registro exitoso! Ya puedes iniciar sesión con tus credenciales.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/home")
@login_required
def home():
    """Pantalla principal según el rol del usuario."""

    tickets_lista = []

    # Si es soporte o administrador, cargar los tickets
    if session.get("rol") in ("soporte", "admin"):

        conn = database.get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                t.id,
                t.descripcion,
                t.categoria,
                t.prioridad,
                t.estado,
                t.creado_en,
                u.nombre AS usuario_nombre,
                u.email AS usuario_email
            FROM tickets t
            JOIN usuarios u ON t.usuario_id = u.id
            ORDER BY t.creado_en DESC
        """)

        tickets_lista = cursor.fetchall()
        conn.close()

    return render_template(
        "home.html",
        tickets=tickets_lista
    )


def clasificar_ticket(descripcion):
    """
    Clasificación automática simulada.
    Posteriormente será reemplazada por un modelo de Machine Learning.
    """

    texto = descripcion.lower()

    # Categoría y prioridad por defecto
    categoria = "Software"
    prioridad = "Media"

    # -------------------------
    # HARDWARE
    # -------------------------

    if any(palabra in texto for palabra in [
        "computadora",
        "computador",
        "pc",
        "laptop",
        "monitor",
        "teclado",
        "mouse",
        "pantalla",
        "no enciende"
    ]):
        categoria = "Hardware"


    # -------------------------
    # REDES
    # -------------------------

    elif any(palabra in texto for palabra in [
        "internet",
        "wifi",
        "wi-fi",
        "red",
        "conexion",
        "conexión",
        "router"
    ]):
        categoria = "Redes"


    # -------------------------
    # IMPRESORAS
    # -------------------------

    elif any(palabra in texto for palabra in [
        "impresora",
        "imprimir",
        "impresión",
        "impresion",
        "cartucho",
        "toner",
        "tóner"
    ]):
        categoria = "Impresoras"


    # -------------------------
    # SOFTWARE
    # -------------------------

    elif any(palabra in texto for palabra in [
        "programa",
        "aplicacion",
        "aplicación",
        "software",
        "sistema",
        "error",
        "windows"
    ]):
        categoria = "Software"


    # -------------------------
    # PRIORIDAD ALTA
    # -------------------------

    if any(palabra in texto for palabra in [
        "urgente",
        "urgencia",
        "emergencia",
        "crítico",
        "critico",
        "muy importante",
        "no funciona",
        "no enciende",
        "quemado"
    ]):
        prioridad = "Alta"


    # -------------------------
    # PRIORIDAD BAJA
    # -------------------------

    elif any(palabra in texto for palabra in [
        "cuando puedan",
        "sin urgencia",
        "no es urgente"
    ]):
        prioridad = "Baja"


    return categoria, prioridad

@app.route("/tickets/crear", methods=["POST"])
@login_required
def crear_ticket():
    """Crea un nuevo ticket enviado por un cliente."""

    # Solo los clientes pueden crear tickets
    if session.get("rol") != "cliente":
        flash("Solo los clientes pueden crear tickets.", "danger")
        return redirect(url_for("home"))

    descripcion = request.form.get("descripcion", "").strip()

    if not descripcion:
        flash("Por favor describe el problema.", "warning")
        return redirect(url_for("home"))

    conn = database.get_db()
    cursor = conn.cursor()

    # Clasificar el ticket
    categoria, prioridad = clasificar_ticket(descripcion)

    # Guardar el ticket
    cursor.execute("""
    INSERT INTO tickets (
        usuario_id,
        descripcion,
        categoria,
        prioridad,
        estado
    )
    VALUES (?, ?, ?, ?, ?)
""", (
    session["user_id"],
    descripcion,
    categoria,
    prioridad,
    "Pendiente"
))

    conn.commit()
    conn.close()

    flash("¡Ticket creado correctamente!", "success")

    return redirect(url_for("home"))

@app.route("/tickets")
@login_required
def tickets():
    """Muestra los tickets al personal de soporte."""

    # Solo soporte y administradores pueden consultar todos los tickets
    if session.get("rol") not in ("soporte", "admin"):
        flash("No tienes permiso para consultar los tickets.", "danger")
        return redirect(url_for("home"))

    conn = database.get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            t.descripcion,
            t.categoria,
            t.prioridad,
            t.estado,
            t.creado_en,
            u.nombre AS usuario_nombre,
            u.email AS usuario_email
        FROM tickets t
        JOIN usuarios u ON t.usuario_id = u.id
        ORDER BY t.creado_en DESC
    """)

    tickets_lista = cursor.fetchall()
    conn.close()

    return render_template(
        "home.html",
        tickets=tickets_lista
    )

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión satisfactoriamente.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
