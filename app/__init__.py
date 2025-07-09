from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'miclave'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['WTF_CSRF_ENABLED'] = True  # CSRF activado para formularios

db = SQLAlchemy(app)
csrf = CSRFProtect(app)


from app import routes, models
