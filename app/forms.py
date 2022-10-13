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
    Regexp
)  # dont worry if pycharm gives a warning here
from app.models import User, Tournament, League
from flask_wtf.file import FileField
from datetime import date


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

"""
I set up validators for all tournament creation fields. For tournament name, it must be unique, has to have something inside the field, and can only
be letters, numbers, dashes and underscores. Tournament location has the same, except it doesnt have to be unique. Might set
regex for tournament league in the future, but for now, it can be empty, but it still has the same regex as others. Tournament date
must be set in the present or future, users should not be able to make a tournament in the past. 
"""
class TournamentCreationForm(FlaskForm):
    tournamentName = StringField("Tournament Name", validators=[DataRequired(), Regexp(regex=r'[ A-Za-z0-9_-]*$')])
    tournamentLocation = StringField("Tournament Location", validators=[DataRequired(), Regexp(regex=r'[ A-Za-z0-9_-]*$')])
    tournamentLeague = StringField("Or Create A New League", validators=[Regexp(regex=r'[ A-Za-z0-9_-]*$')])
    tournamentDate = DateField(
        "TournamentDate", format="%Y-%m-%d", validators=[DataRequired()]    
    )

    def validate_tournamentDate(form, tournamentDate):
        if tournamentDate.data < date.today():
            raise ValidationError("Date must be set in the future.")

    def validate_tournamentName(form, tournamentName):
        tournamentString = tournamentName
        if Tournament.query.filter_by(tournamentName=tournamentString.data).first():
            raise ValidationError("Tournament name is already taken. Please choose a different name.")
        

    submit = SubmitField("Create Tournament")
