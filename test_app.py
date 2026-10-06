"""
Pruebas del Sistema de Login y Registro (SmartDispatch)
"""

import time
import unittest
from app import app
import database

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        database.init_db()

    def test_01_tablas_login_existen(self):
        """Verifica que las tablas de roles, usuarios e historial existan."""
        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("roles", tables)
        self.assertIn("usuarios", tables)
        self.assertIn("historial_accesos", tables)
        print("[OK] Tablas de usuarios y roles verificadas.")

    def test_02_registro_nuevo_usuario(self):
        """Registra un nuevo usuario mediante el formulario."""
        email_nuevo = f"user_{int(time.time() * 1000)}@correo.com"
        response = self.client.post("/register", data={
            "nombre": "Prueba Registro",
            "email": email_nuevo,
            "rol": "cliente",
            "empresa": "Pruebas S.A.",
            "telefono": "1234567890",
            "password": "claveSegura123",
            "confirm_password": "claveSegura123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"exitoso", response.data)
        print("[OK] Registro de nuevo usuario exitoso.")

        # Iniciar sesión con la cuenta recién creada
        login_resp = self.client.post("/login", data={
            "email": email_nuevo,
            "password": "claveSegura123"
        }, follow_redirects=True)

        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b"Prueba Registro", login_resp.data)
        print("[OK] Login con la nueva cuenta registrada validado.")

    def test_03_login_cliente_existente(self):
        """Inicia sesión correctamente como cliente precargado."""
        response = self.client.post("/login", data={
            "email": "cliente@smartdispatch.com",
            "password": "cliente123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Carlos Morales", response.data)
        self.assertIn(b"Cliente", response.data)
        print("[OK] Login de cliente exitoso.")

    def test_04_contrasena_incorrecta(self):
        """Valida que rechace contraseñas incorrectas."""
        response = self.client.post("/login", data={
            "email": "cliente@smartdispatch.com",
            "password": "clave_erronea_123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contrase", response.data)
        print("[OK] Rechazo de contraseña incorrecta validado.")

    def test_05_logout(self):
        """Prueba cierre de sesión y redirección a login."""
        self.client.post("/login", data={
            "email": "cliente@smartdispatch.com",
            "password": "cliente123"
        }, follow_redirects=True)

        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Iniciar Sesi", response.data)
        print("[OK] Cierre de sesión validado.")

if __name__ == "__main__":
    unittest.main()
