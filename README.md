# SmartDispatch: clasificación de tickets con Machine Learning

Aplicación web Flask para reportar incidentes de soporte. Un modelo de aprendizaje supervisado de texto predice la categoría del ticket (Hardware, Redes, Impresoras o Software) y su prioridad (Alta, Media o Baja).

## Enfoque de Machine Learning

- **Tipo:** clasificación supervisada de texto.
- **Preparación:** TF-IDF transforma descripciones en características numéricas, incluyendo unigramas y bigramas.
- **Algoritmo:** regresión logística, con un clasificador independiente para categoría y prioridad.
- **Datos:** `ml/tickets_ejemplo.csv`, un conjunto de ejemplos etiquetados incluido para demostración.
- **Integración:** al crear un ticket, Flask carga el modelo y guarda las dos predicciones en SQLite.

El CSV es pequeño y didáctico, no representa datos reales ni permite afirmar una precisión de producción. Para un resultado confiable, reemplaza o amplía los ejemplos con tickets reales anonimizados y etiquetas revisadas por personal de soporte. Se recomienda evaluar con un conjunto de prueba separado antes de usarlo para decisiones operativas.

## Paneles por rol

- **Cliente:** crea reportes y consulta el estado y la clasificación de sus propios tickets.
- **Soporte:** revisa la cola completa y cambia cada ticket entre Pendiente, En proceso y Resuelto.
- **Administrador:** consulta métricas generales, categorías detectadas, usuarios registrados y todos los tickets; también puede actualizar su estado.

El formulario público solo permite crear cuentas de cliente o soporte. La cuenta de administrador de demostración se crea mediante la inicialización local de la base de datos.

## Requisitos

- Python 3.9 o posterior
- Dependencias indicadas en `requirements.txt`

## Instalación y ejecución

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_model.py
python app.py
```

Abre `http://127.0.0.1:5000`. La base de datos SQLite y las cuentas de demostración se inicializan automáticamente. Para iniciar sesión:

- Cliente: `cliente@smartdispatch.com` / `cliente123`
- Soporte: `soporte@smartdispatch.com` / `soporte123`
- Administrador: `admin@smartdispatch.com` / `admin123`

El modelo se guarda en `ml/modelo_tickets.joblib`. Si no existe, la aplicación lo entrena automáticamente al procesar el primer ticket. Para volver a entrenarlo después de editar el CSV, ejecuta `python train_model.py`.

## Estructura

```text
app.py                  Aplicación Flask y flujo de tickets
database.py             Inicialización y acceso a SQLite
schema.sql              Esquema de usuarios, roles y tickets
ml/clasificador.py      Entrenamiento e inferencia del modelo
ml/tickets_ejemplo.csv Datos de ejemplo etiquetados
train_model.py          Comando para entrenar el modelo
templates/              Vistas HTML
```

## Mejoras para una evaluación académica

1. Reunir tickets anonimizados con categoría y prioridad verificadas.
2. Separar entrenamiento y prueba de forma estratificada.
3. Reportar precisión, recall y F1 por clase, además de una matriz de confusión.
4. Comparar el modelo con una línea base y documentar errores frecuentes.
5. Reentrenar con tickets resueltos y monitorear cambios en la calidad.
