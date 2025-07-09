from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class PrediccionForm(FlaskForm):
    sepal_length = FloatField('Longitud Sépalo', validators=[DataRequired()])
    sepal_width = FloatField('Ancho Sépalo', validators=[DataRequired()])
    petal_length = FloatField('Longitud Pétalo', validators=[DataRequired()])
    petal_width = FloatField('Ancho Pétalo', validators=[DataRequired()])
    submit = SubmitField('Predecir')
