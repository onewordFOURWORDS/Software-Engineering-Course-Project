from flask_wtf import FlaskForm  # dont worry if pycharm gives a warning here
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    DateField,
    SelectField
)  # dont worry if pycharm gives a warning here
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
)  # dont worry if pycharm gives a warning here
from app.models import User


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
    tournamentName = StringField("TournamentName", validators=[DataRequired()])
    tournamentLocation = StringField("TournamentLocation", validators=[DataRequired()])
    tournamentDate = DateField(
        "TournamentDate", format="%Y-%m-%d", validators=[DataRequired()]
    )
    submit = SubmitField("Create Tournament")


class RequestPermissionForm(FlaskForm):
    request_coach = BooleanField("Make me a coach!")
    request_admin = BooleanField("Make me an admin!")
    remove_coach = BooleanField("Un-Make me a coach!")
    remove_admin = BooleanField("Un-Make me an admin!")
    submit = SubmitField("Submit changes")


class ManualPermissionsForm(FlaskForm):
    userID = IntegerField("User ID", validators=[DataRequired()])
    actions = SelectField("permission actions", choices=[(1,'approve coach'),(2, 'deny coach'),(3, 'approve admin'),(4, 'deny admin')])
    submit = SubmitField("Submit changes")


