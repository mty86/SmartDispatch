-- ==========================================================
-- BASE DE DATOS: SmartDispatch - Módulo de Login
-- Autenticación de Clientes y Personal de Soporte
-- ==========================================================

-- 1. TABLA DE ROLES
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

-- 2. TABLA DE USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rol_id INTEGER NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    empresa VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'activo', -- 'activo', 'bloqueado'
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles (id) ON DELETE RESTRICT
);

-- 3. TABLA DE AUDITORÍA / HISTORIAL DE INICIOS DE SESIÓN
CREATE TABLE IF NOT EXISTS historial_accesos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    ip_origen VARCHAR(45),
    user_agent TEXT,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

-- ==========================================================
-- ÍNDICE PARA BÚSQUEDA RÁPIDA POR CORREO
-- ==========================================================
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
