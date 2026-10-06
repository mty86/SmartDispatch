"""
Módulo de Base de Datos para SmartDispatch
Gestiona la conexión y usuarios para el sistema de Login.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smartdispatch.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

def get_db():
    """Obtiene una conexión a la base de datos con row_factory como diccionario."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Crea las tablas a partir del archivo schema.sql y siembra los usuarios de login."""
    conn = get_db()
    cursor = conn.cursor()

    # Ejecutar esquema de tablas
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    # 1. Sembrar roles de usuario
    roles_iniciales = [
        ('cliente', 'Usuario cliente con acceso al portal'),
        ('soporte', 'Agente o técnico de soporte'),
        ('admin', 'Administrador general del sistema')
    ]
    for nombre, desc in roles_iniciales:
        cursor.execute("""
            INSERT OR IGNORE INTO roles (nombre, descripcion)
            VALUES (?, ?)
        """, (nombre, desc))

    cursor.execute("SELECT id, nombre FROM roles")
    roles = {row['nombre']: row['id'] for row in cursor.fetchall()}

    # 2. Sembrar usuarios de prueba con contraseña encriptada
    usuarios_demo = [
        {
            "nombre": "Carlos Morales",
            "email": "cliente@smartdispatch.com",
            "password": "cliente123",
            "rol_id": roles["cliente"],
            "telefono": "+52 55 1234 5678",
            "empresa": "Logística Norte S.A."
        },
        {
            "nombre": "Ana Martínez",
            "email": "soporte@smartdispatch.com",
            "password": "soporte123",
            "rol_id": roles["soporte"],
            "telefono": "+52 55 8765 4321",
            "empresa": "Mesa de Soporte SmartDispatch"
        },
        {
            "nombre": "Administrador Principal",
            "email": "admin@smartdispatch.com",
            "password": "admin123",
            "rol_id": roles["admin"],
            "telefono": "+52 55 9999 0000",
            "empresa": "SmartDispatch HQ"
        }
    ]

    for u in usuarios_demo:
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (u["email"],))
        existente = cursor.fetchone()
        if not existente:
            p_hash = generate_password_hash(u["password"])
            cursor.execute("""
                INSERT INTO usuarios (rol_id, nombre, email, password_hash, telefono, empresa)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (u["rol_id"], u["nombre"], u["email"], p_hash, u["telefono"], u["empresa"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos de login inicializada en:", DB_PATH)
