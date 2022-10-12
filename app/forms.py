from flask_wtf import FlaskForm  # dont worry if pycharm gives a warning here
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    DateField,
)  # dont worry if pycharm gives a warning here
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
)  # dont worry if pycharm gives a warning here
from app.models import User
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class TeamCreation(FlaskForm):
    teamname = StringField("Team Name", validators=[DataRequired()])
    coachID = IntegerField("Username", validators=[DataRequired()])
    submit = SubmitField("Submit New Team")
    # league = db.Column(db.Integer, db.ForeignKey('league.id'))


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class TournamentCreationForm(FlaskForm):
    tournamentName = StringField("Tournament Name", validators=[DataRequired()])
    tournamentLocation = StringField("Tournament Location", validators=[DataRequired()])
    tournamentLeague = StringField("Or Create A New League")
    tournamentDate = DateField(
        "TournamentDate", format="%Y-%m-%d", validators=[DataRequired()]
    )
    tournamentPicture = FileField("Tournament Picture")
    submit = SubmitField("Create Tournament")
