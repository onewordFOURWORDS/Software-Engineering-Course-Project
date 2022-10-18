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
Keeping tournament name not unique for now. In the future, might want to make it unique with date and league.
Tournament location has the same, except it doesnt have to be unique. Might set
regex for tournament league in the future, but for now, it can be empty, but it still has the same regex as others. Tournament date
must be set in the present or future, users should not be able to make a tournament in the past. League has to be unique if they 
are creating one.
"""
class TournamentCreationForm(FlaskForm):
    tournamentName = StringField("Tournament Name", validators=[DataRequired(), Regexp(regex=r'[ \'A-Za-z0-9]*$', message="Tournament name must not contain any special characters.")])
    tournamentLocation = StringField("Tournament City", validators=[DataRequired(), Regexp(regex=r'[ \'A-Za-z0-9]*$', message="City name must not contain any special characters.")])
    tournamentLeague = StringField("Or Create A New League", validators=[Regexp(regex=r'[ \'A-Za-z0-9]*$', message="League name must not contain any special characters.")], render_kw={"placeholder": "Please leave empty if you do not wish to create a league!"})
    tournamentDate = DateField(
        "TournamentDate", format="%Y-%m-%d", validators=[DataRequired()]    
    )

    def validate_tournamentDate(form, tournamentDate):
        if tournamentDate.data < date.today():
            raise ValidationError("Date must be set in the future.")

    def validate_tournamentLeague(form, tournamentLeague):
        leagueString = tournamentLeague
        if League.query.filter_by(leagueName=leagueString.data).first():
            raise ValidationError("League already exists. Choose existing league or create a unique league. ")
        

    submit = SubmitField("Create Tournament")


class SearchByDate(FlaskForm):
    """
    A search bar to filter tournaments by date. Leaving end date blank will show all upcoming tournaments.
    """
    startDate = DateField("StartDate", format="%Y-%m-%d", validators=[DataRequired()])
    endDate = DateField("EndDate", format="%Y-%m-%d")


    def validate_dates(form, startDate, endDate):
        if endDate.data is None:
            return
        elif endDate.data < startDate:
            raise ValidationError("Start date must be before end date.")
    

    submit = SubmitField("Search")
