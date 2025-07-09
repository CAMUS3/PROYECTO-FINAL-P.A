from flask import render_template, request, jsonify
from app import app, db, csrf
from app.forms import PrediccionForm
from app.models import Prediccion
import joblib
import numpy as np
from sqlalchemy import inspect

# Cargar modelo de ML
modelo = joblib.load("app/ml_model/modelo.pkl")

# ---------------------- Interfaz Web ----------------------
@app.route("/", methods=["GET", "POST"])
def index():
    form = PrediccionForm()
    if form.validate_on_submit():
        datos = np.array([[form.sepal_length.data, form.sepal_width.data,
                           form.petal_length.data, form.petal_width.data]])
        pred = modelo.predict(datos)[0]
        especie = ["Setosa", "Versicolor", "Virginica"][pred]

        # Guardar en base de datos
        prediccion = Prediccion(
            sepal_length=form.sepal_length.data,
            sepal_width=form.sepal_width.data,
            petal_length=form.petal_length.data,
            petal_width=form.petal_width.data,
            resultado=especie
        )
        db.session.add(prediccion)
        db.session.commit()

        return render_template("resultado.html", especie=especie)

    return render_template("index.html", form=form)


# ---------------------- API POST ----------------------
@csrf.exempt
@app.route("/api/predicciones", methods=["POST"])
def crear_prediccion():
    if request.content_type != 'application/json':
        return jsonify({"error": "Solo se acepta JSON"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    try:
        datos = np.array([[data['sepal_length'], data['sepal_width'],
                           data['petal_length'], data['petal_width']]])
        pred = modelo.predict(datos)[0]
        especie = ["Setosa", "Versicolor", "Virginica"][pred]

        prediccion = Prediccion(
            sepal_length=data['sepal_length'],
            sepal_width=data['sepal_width'],
            petal_length=data['petal_length'],
            petal_width=data['petal_width'],
            resultado=especie
        )
        db.session.add(prediccion)
        db.session.commit()

        return jsonify({"resultado": especie}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------- API GET ----------------------
@app.route("/api/predicciones", methods=["GET"])
def get_predicciones():
    predicciones = Prediccion.query.all()
    return jsonify([
        {
            "id": p.id,
            "sepal_length": p.sepal_length,
            "sepal_width": p.sepal_width,
            "petal_length": p.petal_length,
            "petal_width": p.petal_width,
            "resultado": p.resultado
        } for p in predicciones
    ])


# ---------------------- Verificación ----------------------
@app.route("/verificar")
def verificar():
    tablas = inspect(db.engine).get_table_names()
    return f"Tablas en la base de datos: {tablas}"
