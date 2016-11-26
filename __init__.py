from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)

db = SQLAlchemy(app)

from Lab_Journal import views
from Lab_Journal import models

db.create_all()
