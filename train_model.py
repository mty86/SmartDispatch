"""Entrena el clasificador de tickets con los ejemplos de ml/tickets_ejemplo.csv."""

from ml.clasificador import MODEL_PATH, entrenar_modelo


if __name__ == "__main__":
    paquete = entrenar_modelo()
    print(f"Modelo entrenado con {paquete['n_ejemplos']} tickets: {MODEL_PATH}")
