from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    DateField,
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
)
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class TeamCreationForm(FlaskForm):
    team_name = StringField("Team Name", validators=[DataRequired()])
    user_is_coach = BooleanField("I will be coaching this team:", default="checked")

    # coachID = IntegerField(
    #     "Username", validators=[DataRequired()]
    # )  # I have no idea why deleting this breaks the form atm. This is tightly linked with models and the sqlalchemy definitions,
    # has something to do with what's being expected there.
    submit = SubmitField("Register")
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
    tournamentName = StringField("TournamentName", validators=[DataRequired()])
    tournamentLocation = StringField("TournamentLocation", validators=[DataRequired()])
    tournamentDate = DateField(
        "TournamentDate", format="%Y-%m-%d", validators=[DataRequired()]
    )
    submit = SubmitField("Create Tournament")
