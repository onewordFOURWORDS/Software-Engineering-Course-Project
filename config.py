import os

basedir = os.path.abspath(os.path.dirname(__file__))


# Need to set ENV VARIABLES on Heroku, this approach should more or less still worK?
# and this file can be in the repo then, that's fine?
class Config(object):
    SECRET_KEY = os.environ.get("SSBM_SECRET_KEY")
    # postgres 15 defaults to 5433, postgres 14 to 5432, I believe.
    # PORT_NUMBER = os.environ.get("SSBM_DB_PORT_NUMBER")
    # DB_NAME = "app"
    # DB_NAME = os.environ.get("DB_NAME")
    # DB_USER = "postgres"
    # DB_USER = os.environ.get("DB_USER")

    SQLALCHEMY_DATABASE_URI = (
        # f"postgresql://{DB_USER}:{SECRET_KEY}@localhost:{PORT_NUMBER}/{DB_NAME}"
        os.environ.get("DATABASE_URL")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Email Configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["support@supersickbracketmaker.tech"]
    # Selenium configuration
    SEL_PATH = os.environ.get("SEL_PATH")
