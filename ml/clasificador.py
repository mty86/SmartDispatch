"""Clasificador supervisado de categoría y prioridad de tickets."""

import csv
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "tickets_ejemplo.csv"
MODEL_PATH = BASE_DIR / "modelo_tickets.joblib"


def entrenar_modelo():
    """Entrena dos modelos TF-IDF + regresión logística con el CSV etiquetado."""
    with DATA_PATH.open(encoding="utf-8", newline="") as archivo:
        filas = list(csv.DictReader(archivo))

    if len(filas) < 8:
        raise ValueError("Se requieren al menos 8 ejemplos etiquetados para entrenar.")

    textos = [fila["descripcion"].strip() for fila in filas]
    if any(not texto for texto in textos):
        raise ValueError("El conjunto de datos contiene descripciones vacías.")

    modelos = {}
    for objetivo in ("categoria", "prioridad"):
        etiquetas = [fila[objetivo].strip() for fila in filas]
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(lowercase=True, strip_accents="unicode", ngram_range=(1, 2))),
            ("clasificador", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ])
        pipeline.fit(textos, etiquetas)
        modelos[objetivo] = pipeline

    paquete = {"modelos": modelos, "n_ejemplos": len(filas), "version": 1}
    joblib.dump(paquete, MODEL_PATH)
    return paquete


def cargar_modelo():
    """Carga el modelo guardado y lo entrena automáticamente si aún no existe."""
    if not MODEL_PATH.exists():
        return entrenar_modelo()
    return joblib.load(MODEL_PATH)


def clasificar_ticket(descripcion):
    """Devuelve categoría y prioridad estimadas a partir del texto del ticket."""
    texto = " ".join((descripcion or "").split())
    if not texto:
        raise ValueError("La descripción del ticket no puede estar vacía.")

    paquete = cargar_modelo()
    return (
        paquete["modelos"]["categoria"].predict([texto])[0],
        paquete["modelos"]["prioridad"].predict([texto])[0],
    )
