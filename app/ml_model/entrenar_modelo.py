import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Cargar dataset de enfermedades cardíacas desde sklearn
from sklearn.datasets import load_iris  # Usamos Iris como demo
iris = load_iris()
X = iris.data
y = iris.target

# Entrenar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Guardar modelo entrenado
joblib.dump(modelo, "app/ml_model/modelo.pkl")
print("Modelo guardado correctamente.")
