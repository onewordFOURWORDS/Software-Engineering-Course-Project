from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from jinja2 import Environment, FileSystemLoader
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
mail = Mail(app)

from app.models import *

with app.app_context():
    db.create_all()

env = Environment(loader=FileSystemLoader("./app/templates"))
env.globals["is_admin"] = User.is_admin
env.globals["is_coach"] = User.is_coach


# Scott's testing db setup stuff. Uncomment if thou desire cat.
# user = User.query.filter_by(username='admin').first()
# if not user:
# rebuild_users()

from app import routes
