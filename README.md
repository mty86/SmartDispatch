# SmartDispatch - Sistema de Login y Registro (Cliente y Soporte)

Sistema de autenticación con inicio de sesión y registro de usuarios para **Clientes** y **Personal de Soporte**, desarrollado en **Python (Flask)** con base de datos relacional **SQLite** y script **SQL** (`schema.sql`).

---

## 🚀 Cómo Iniciar la Aplicación

### 1. Iniciar el servidor web
Abre una terminal en esta carpeta y ejecuta:
```powershell
.\venv\Scripts\python.exe app.py
```

### 2. Abrir en el navegador
Ingresa a: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## ✨ Funcionalidades

1. **Inicio de Sesión Limpio:** Formulario estándar de Correo y Contraseña sin botones de prueba rápida expuestos.
2. **Registro de Usuarios:** Enlace directo **"¿No tienes una cuenta? Regístrate aquí"** en el login para crear cuentas eligiendo el rol:
   * **Cliente:** Para usuarios que reportan o solicitan soporte.
   * **Personal de Soporte:** Para técnicos y agentes de soporte.
3. **Cifrado Seguro:** Contraseñas protegidas mediante hash PBKDF2/SHA-256 (`werkzeug.security`).
4. **Base de Datos Automática:** SQLite en `smartdispatch.db` con script exportable en `schema.sql`.

---

## 🗄️ Base de Datos

*   **Archivo SQLite:** [`smartdispatch.db`](smartdispatch.db)
*   **Script DDL de tablas:** [`schema.sql`](schema.sql)
*   **Módulo de conexión y arranque:** [`database.py`](database.py)

### Tablas:
*   `roles`: `cliente`, `soporte`, `admin`.
*   `usuarios`: Registro de nombres, correo, teléfono, empresa, rol y contraseña cifrada.
*   `historial_accesos`: Auditoría de logins (IP, fecha y User-Agent).

---

## 🧪 Pruebas Automatizadas
```powershell
.\venv\Scripts\python.exe test_app.py
```
Resultado: **5 pruebas unitarias exitosas** (registro, login, validaciones de seguridad y sesión).
