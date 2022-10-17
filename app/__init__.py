from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

# Register permissions functions here so they can be used
# within Jinja templates
from app.models import *

env = Environment(loader=FileSystemLoader("./app/templates"))
env.globals["is_admin"] = User.is_admin
env.globals["is_coach"] = User.is_coach

# TODO: figure out a better way to handle this, currently
# need this in the db for the way we do the no team thing on user registration.
# no_team = Team(id=0)
# db.session.add(no_team)
# db.session.commit()

from app import routes

"""The script above simply creates the application object as an instance of class Flask imported from the flask 
package. The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of 
the module in which it is used. Flask uses the location of the module passed here as a starting point when it needs 
to load associated resources such as template files, which I will cover in Chapter 2. For all practical purposes, 
passing __name__ is almost always going to configure Flask in the correct way. The application then imports the 
routes module, which doesn't exist yet. 

One aspect that may seem confusing at first is that there are two entities named app. The app package is defined by 
the app directory and the __init__.py script, and is referenced in the from app import routes statement. The app 
variable is defined as an instance of class Flask in the __init__.py script, which makes it a member of the app 
package. 

Another peculiarity is that the routes module is imported at the bottom and not at the top of the script as it is 
always done. The bottom import is a workaround to circular imports, a common problem with Flask applications. You are 
going to see that the routes module needs to import the app variable defined in this script, so putting one of the 
reciprocal imports at the bottom avoids the error that results from the mutual references between these two files. """
