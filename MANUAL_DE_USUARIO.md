# 📘 Manual de Usuario - Sistema de Autenticación SmartDispatch

Bienvenido al **Manual de Usuario** del sistema de autenticación y gestión de acceso de **SmartDispatch**. Este documento describe el propósito del sistema, los pasos para ejecutar la aplicación, cómo registrar nuevas cuentas, iniciar sesión y administrar perfiles de usuario.

---

## 📑 Tabla de Contenidos
1. [Introducción y Objetivos](#1-introducción-y-objetivos)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación y Puesta en Marcha](#3-instalación-y-puesta-en-marcha)
4. [Roles del Sistema](#4-roles-del-sistema)
5. [Guía de Uso Paso a Paso](#5-guía-de-uso-paso-a-paso)
   - [5.1 Inicio de Sesión (Login)](#51-inicio-de-sesión-login)
   - [5.2 Registro de Nuevos Usuarios](#52-registro-de-nuevos-usuarios)
   - [5.3 Pantalla de Bienvenida y Perfil](#53-pantalla-de-bienvenida-y-perfil)
   - [5.4 Cierre de Sesión Seguro (Logout)](#54-cierre-de-sesión-seguro-logout)
6. [Cuentas Demo Preconfiguradas](#6-cuentas-demo-preconfiguradas)
7. [Base de Datos y Seguridad](#7-base-de-datos-y-seguridad)
8. [Preguntas Frecuentes y Solución de Problemas](#8-preguntas-frecuentes-y-solución-de-problemas)
9. [Descarga e Instalación como Aplicación Híbrida (PWA)](#9-descarga-e-instalación-como-aplicación-híbrida-pwa)

---

## 1. Introducción y Objetivos

**SmartDispatch** es una plataforma web desarrollada con **Python (Flask)** y **SQLite** diseñada para gestionar el acceso seguro de usuarios diferenciados entre **Clientes** y **Personal de Soporte Técnico**.

### Características principales:
* **Autenticación Segura:** Validación de credenciales con hashing de contraseñas PBKDF2/SHA-256.
* **Control de Acceso basado en Roles (RBAC):** Clasificación de usuarios según su función.
* **Diseño Flotante y Moderno:** Interfaz responsiva centrada con estilos de sombras (`box-shadow`) y Tailwind CSS.
* **Auditoría de Inicios de Sesión:** Registro automático de dirección IP, fecha/hora y navegador.

---

## 2. Requisitos del Sistema

Para ejecutar el sistema en un entorno local se necesita:
* **Sistema Operativo:** Windows 10/11, macOS o Linux.
* **Python:** Versión 3.10 o superior (el proyecto incluye su propio entorno virtual `venv`).
* **Navegador Web:** Google Chrome, Microsoft Edge, Mozilla Firefox o Safari.

---

## 3. Instalación y Puesta en Marcha

Sigue estos sencillos pasos para iniciar la aplicación:

### Paso 1: Abrir la terminal
Abre **PowerShell** o el símbolo del sistema en la carpeta del proyecto `SmartDispatch`.

### Paso 2: Iniciar el servidor
Ejecuta el siguiente comando:
```powershell
.\venv\Scripts\python.exe app.py
```

Deberás ver un mensaje similar a:
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Paso 3: Abrir en el navegador
Ingresa en tu navegador web a la siguiente dirección:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)** (o `http://localhost:5000`)

---

## 4. Roles del Sistema

El sistema categoriza a los usuarios en tres roles:

| Rol | Descripción |
| :--- | :--- |
| **Cliente** | Usuario final o cliente empresarial que utiliza el portal para solicitar asistencia técnica. |
| **Personal de Soporte** | Técnico o agente encargado de atender solicitudes, diagnósticos y asistencia. |
| **Administrador** | Administrador del sistema con control global de cuentas y configuración. |

---

## 5. Guía de Uso Paso a Paso

### 5.1 Inicio de Sesión (Login)
1. Al acceder a la página web, el sistema te redirigirá automáticamente a la pantalla de **Iniciar Sesión** (`/login`).
2. Ingresa tu **Correo Electrónico** en el campo correspondiente.
3. Ingresa tu **Contraseña**.
4. Haz clic en el botón azul **"Iniciar Sesión"**.

> **Validaciones:**
> * Si el correo no existe, el sistema mostrará: *"Correo electrónico no encontrado."*
> * Si la contraseña es incorrecta, el sistema alertará: *"Contraseña incorrecta."*
> * Si faltan campos por llenar, te solicitará completarlos.

---

### 5.2 Registro de Nuevos Usuarios
Si aún no dispones de una cuenta en el sistema:

1. En la parte inferior de la tarjeta de inicio de sesión, haz clic en el enlace **"Regístrate aquí"**.
2. Completa los campos del formulario de registro:
   * **Nombre Completo:** Tu nombre o el nombre del contacto responsable.
   * **Correo Electrónico:** Dirección de correo institucional o personal (debe ser única).
   * **Tipo de Usuario (Rol):** Selecciona entre **Cliente** o **Personal de Soporte**.
   * **Empresa / Departamento:** Nombre de tu empresa o área técnica.
   * **Teléfono de Contacto:** Número telefónico opcional para asistencia.
   * **Contraseña:** Mínimo 6 caracteres.
   * **Confirmar Contraseña:** Repite exactamente la misma contraseña.
3. Haz clic en **"Crear Cuenta"**.
4. El sistema guardará al usuario en la base de datos y te redirigirá a la pantalla de login con el mensaje:
   * *"¡Registro exitoso! Ya puedes iniciar sesión con tus credenciales."*

---

### 5.3 Pantalla de Bienvenida y Perfil
Una vez autenticado exitosamente, el sistema te dirigirá a tu panel personal (`/home`):
* Muestra el mensaje de **¡Sesión Iniciada!**
* Visualiza la tarjeta con tus datos:
  * **Nombre del usuario**.
  * **Correo registrado**.
  * **Insignia del Rol** (verde para Cliente, azul para Soporte, morada para Admin).
  * **Empresa o Departamento**.

---

### 5.4 Cierre de Sesión Seguro (Logout)
1. Para finalizar tu sesión y evitar accesos no autorizados en tu equipo, haz clic en el botón rojo **"Cerrar Sesión"**.
2. El sistema destruirá la sesión activa de forma segura y te regresará al inicio de sesión.

---

## 6. Cuentas Demo Preconfiguradas

Para agilizar pruebas y demostraciones, la base de datos incluye tres cuentas listas para usar:

| Perfil | Correo Electrónico | Contraseña | Rol Asignado |
| :--- | :--- | :--- | :--- |
| **Cliente de Demostración** | `cliente@smartdispatch.com` | `cliente123` | Cliente (`Logística Norte S.A.`) |
| **Técnico de Soporte** | `soporte@smartdispatch.com` | `soporte123` | Soporte (`Mesa de Soporte SmartDispatch`) |
| **Administrador** | `admin@smartdispatch.com` | `admin123` | Administrador (`SmartDispatch HQ`) |

---

## 7. Base de Datos y Seguridad

### ¿Dónde se almacenan los datos?
* **Base de datos física:** En el archivo `smartdispatch.db` ubicado en la carpeta principal.
* **Modelo relacional:** Definido en `schema.sql` con claves foráneas, índices y tablas:
  * `roles`: Definición de perfiles.
  * `usuarios`: Datos generales y contraseñas.
  * `historial_accesos`: Registro de auditoría cada vez que un usuario ingresa (IP, navegador y marca de tiempo).

### Seguridad de Contraseñas
Las contraseñas **nunca se guardan en texto plano**. Se procesan mediante funciones criptográficas de una sola vía (hash con sal) utilizando la librería `werkzeug.security`.

---

## 8. Preguntas Frecuentes y Solución de Problemas

### ❓ ¿Qué hacer si aparece "Address already in use" o el puerto 5000 está ocupado?
Si el puerto 5000 está tomado por otra instancia de Python, cierra la ventana anterior de la consola o ejecuta en PowerShell:
```powershell
Get-Process python* | Stop-Process
```
Y luego vuelve a ejecutar `.\venv\Scripts\python.exe app.py`.

### ❓ ¿Cómo restablecer la base de datos a su estado original?
Si deseas borrar todos los usuarios de prueba y volver a iniciar de cero:
1. Elimina el archivo `smartdispatch.db`.
2. Ejecuta:
   ```powershell
   .\venv\Scripts\python.exe database.py
   ```
La base de datos se recreará limpia e inicializada en segundos.

### ❓ ¿Cómo verificar que el sistema funciona correctamente?
Puedes correr la suite de pruebas unitarias automatizadas con:
```powershell
.\venv\Scripts\python.exe test_app.py
```
Deberás obtener `OK` (8 pruebas exitosas).

---

## 9. Descarga e Instalación como Aplicación Híbrida (PWA)

SmartDispatch cuenta con soporte para **PWA (Progressive Web App)**, lo que permite instalar la plataforma como una **aplicación de escritorio o móvil independiente**, funcionando en su propia ventana sin barras de direcciones del navegador.

### 💻 Instalación en Computadora (Windows / Mac con Chrome o Edge):
1. Inicia la aplicación e ingresa a `http://127.0.0.1:5000`.
2. Haz clic en el botón flotante inferior derecho **"📲 Descargar / Instalar App"**, o bien haz clic en el ícono de instalación (computadora con flecha hacia abajo) que aparece en la parte derecha de la barra de direcciones de tu navegador.
3. En el cuadro de diálogo emergente, selecciona **"Instalar"**.
4. ¡Listo! SmartDispatch se abrirá en una ventana de aplicación nativa y creará un acceso directo en tu Escritorio y Menú Inicio.

### 📱 Instalación en Dispositivos Android:
1. Abre la dirección de SmartDispatch en Google Chrome desde tu teléfono.
2. Toca el botón flotante **"Descargar / Instalar App"** o el menú de tres puntos (⋮) en la esquina superior derecha.
3. Selecciona **"Instalar aplicación"** o **"Agregar a la pantalla principal"**.
4. La aplicación se instalará con su propio ícono en tu pantalla de inicio como una app móvil.

### 🍎 Instalación en iPhone / iPad (iOS Safari):
1. Abre SmartDispatch en el navegador Safari.
2. Toca el botón de **Compartir** (ícono de cuadro con flecha hacia arriba).
3. Desliza hacia abajo y presiona **"Agregar a la pantalla de inicio"**.
4. Toca **"Agregar"** en la esquina superior derecha.

