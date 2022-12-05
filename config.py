import os

basedir = os.path.abspath(os.path.dirname(__file__))


# TODO: Figure out best practice for managing the config file/making sure we keep keys etc out of the repo.
# This is fine for now.
class Config(object):
    SECRET_KEY = os.environ.get("SSBM_SECRET_KEY")
    # postgres 15 defaults to 5433, postgres 14 to 5432, I believe.
    PORT_NUMBER = os.environ.get("SSBM_DB_PORT_NUMBER")
    DB_NAME = "app"
    DB_USER = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{SECRET_KEY}@localhost:{PORT_NUMBER}/{DB_NAME}"
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
