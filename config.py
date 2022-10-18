import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # database uri should look like: postgresql://user:password@localhost:5432/database_name
    # you made need to change some of these variables if you didn't use the default settings when you installed postgres
    # locally.
    PORT_NUMBER = 5433
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
