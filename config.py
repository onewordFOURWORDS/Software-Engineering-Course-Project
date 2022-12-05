import os

basedir = os.path.abspath(os.path.dirname(__file__))


# Need to set ENV VARIABLES on Heroku, this approach should more or less still worK?
# and this file can be in the repo then, that's fine?
class DevConfig(object):
    SECRET_KEY = os.environ.get("SSBM_SECRET_KEY")
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


class ProdConfig(object):
    # "Heroku rotates credentials periodically and updates applications where this database is attached."
    # So we have to do a bit of string processing here:
    db_url = os.environ.get("DATABASE_URL")
    # grab everything between $username: and @ec2..., that's your password
    username_terminator = ":"
    host_string_start = "@"
    SECRET_KEY = db_url.split(username_terminator)[1].split(host_string_start)[0]
    # Can't edit this in Heroku Dashboard but apparently you must use
    # postgres instead of postgresql as of sqlalchemy v1.40
    # see https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy
    # for details
    SQLALCHEMY_DATABASE_URI = db_url.replace("postgres://", "postgresql://", 1)
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
