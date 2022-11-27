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

# Register permissions functions here so they can be used
# within Jinja templates
from app.models import *
with app.app_context():
    db.create_all()

env = Environment(loader=FileSystemLoader("./app/templates"))
env.globals["is_admin"] = User.is_admin
env.globals["is_coach"] = User.is_coach


# if admin user not in db, add to db
# useful for testing, only creates admin if not present


# TODO: figure out a better way to handle this, currently
# need this in the db for the way we do the no team thing on user registration.
# no_team = Team(id=0)
# db.session.add(no_team)
# db.session.commit()

from app import routes

