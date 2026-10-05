# SmartDispatch
# SmartDispatch — Aplicación Web Instalable (PWA) de Clasificación y Asignación Automática de Tickets

## 1. Problemática a resolver
En las empresas de servicios y soporte técnico de campo, la gestión y asignación manual de reportes de incidentes genera cuellos de botella operativos. El tiempo que toma a un operador leer una solicitud, evaluar su urgencia y decidir a qué técnico asignársela incrementa el tiempo de respuesta ante fallas críticas y conduce a asignaciones ineficientes.

## 2. Descripción del proyecto
SmartDispatch es una **Aplicación Web Progresiva (PWA / Web Instalable)** para la clasificación y asignación automática de tickets de soporte técnico. El sistema recibe como entrada la descripción en texto libre de una falla. Mediante un modelo de Procesamiento de Lenguaje Natural (NLP), clasifica automáticamente la urgencia del reporte y asigna la tarea al técnico disponible cuyo historial refleje la mayor tasa de éxito en la resolución de ese tipo de incidentes, actualizando el estado en tiempo real.

## 3. Rama de la Inteligencia Artificial
- **Rama principal:** Procesamiento de Lenguaje Natural (NLP) / Machine Learning Supervisado.
- **Justificación:** Se utiliza NLP para analizar la semántica de la descripción textual del ticket, categorizar el tipo de problema, determinar el nivel de urgencia y emparejar la tarea con el perfil/historial del técnico disponible.

## 4. Caso de uso
- **Usuario objetivo:** Clientes/Usuarios que reportan incidentes y Técnicos de campo.
- **Escenario de uso:** Un usuario abre la Web App (o PWA instalada en su dispositivo) y reporta un fallo (*"El router principal parpadea en rojo y no hay internet en la oficina"*). El backend de NLP determina que se trata de un incidente de **Redes** con urgencia **Alta** y asigna la tarea automáticamente al técnico capacitado más cercano.
- **Resultado esperado:** Asignación inmediata sin intervención humana y notificación en tiempo real al técnico.

## 5. Requisitos del sistema

### Backend y Servicios de IA
- Python 3.9+
- scikit-learn, pandas, numpy, nltk
- Firebase Admin SDK

### Frontend (Web App Instalable / PWA)
- Navegador web moderno (Chrome, Edge, Safari)
- HTML5, CSS3, JavaScript (o framework React/Vue/Svelte)
- Service Workers y Web App Manifest (para función offline e instalación)

---

## 6. Instrucciones de instalación y ejecución

### Opción A: Uso como Aplicación Web Instalable (PWA)
1. Abrir la URL de la aplicación desde cualquier navegador móvil o de escritorio: `https://smartdispatch.web.app` (URL de despliegue).
2. Hacer clic en la barra del navegador en la opción **"Instalar aplicación"** o **"Agregar a la pantalla de inicio"**.
3. Ejecutar la app directamente desde el ícono generado en el escritorio o menú del dispositivo.

### Opción B: Ejecución Local del Servidor/Backend
1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/mty86/SmartDispatch.git](https://github.com/mty86/SmartDispatch.git)
   cd SmartDispatch
