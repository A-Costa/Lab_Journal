from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)

app.permanent_session_lifetime = timedelta(seconds=10)


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



from Lab_Journal import views
from Lab_Journal import models

db.create_all()
