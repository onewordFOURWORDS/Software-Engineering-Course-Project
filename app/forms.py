from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    DateField,
    SelectField,
    FieldList,
    FormField,
    SelectMultipleField,
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Regexp,
    Length,
    InputRequired,
)
from app.models import User, League, Team
from operator import itemgetter
import re


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class TeamCreationForm(FlaskForm):
    team_name = StringField("Team Name", validators=[DataRequired()])
    coaches = User.query.filter_by(is_coach=True)
    coaches_list = []
    for coach in coaches:
        coaches_list.append((coach.id, coach.full_name))
    coach = SelectField("Select your coach: ", choices=coaches_list)
    leagues = League.query.all()
    league_list = []
    for league in leagues:
        league_list.append((league.id, league.league_name))
    league = SelectField("Select your league: ", choices=league_list)
    submit = SubmitField("Register")

    def validate_team_name(self, field):
        team = Team.query.filter_by(team_name=field.data).first()
        if team is not None:
            raise ValidationError("Team name is already taken.")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=32)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=12, max=64)]
    )
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    first_name = StringField("First Name:", validators=[DataRequired()])
    last_name = StringField("Last Name:", validators=[DataRequired()])
    teams = Team.query.all()
    team_list = []
    for team in teams:
        team_list.append((team.id, team.team_name))
    affiliated_team = SelectField(
        "Choose a team to be affiliated with, or select None to set this up later: ",
        choices=sorted(
            team_list, key=itemgetter(0)
        ),  # sort by ID, the first element in each tuple.
        coerce=int,
        validate_choice=False,
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


class LeaguePageTeamSelectForm(FlaskForm):
    teams = Team.query.all()
    team_list = []
    for team in teams:
        if team.id != 0:
            team_list.append((team.id, team.team_name))
    affiliated_team = SelectField(
        "Choose a team to be affiliated with:",
        choices=sorted(
            team_list, key=itemgetter(0)
        ),  # sort by ID, the first element in each tuple.
        coerce=int,
        validators=[DataRequired()],
        validate_choice=False,
    )
    submit = SubmitField("Select Team")


class LeagueCreationForm(FlaskForm):
    league = StringField(
        "Create A New League",
        validators=[
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="League name must not contain any special characters.",
            ),
        ],
        render_kw={"placeholder": "Enter a name for your league."},
    )

    def validate_league(self, league):
        print("validate_league is being called....")
        if League.query.filter_by(league_name=league.data).first():
            raise ValidationError("League already exists. Select a new name.")

    submit = SubmitField("Create League")


class TournamentCreationForm(FlaskForm):
    tournament_name = StringField(
        "Tournament Name",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="Tournament name must not contain any special characters.",
            ),
        ],
    )
    tournament_city = StringField(
        "Tournament City",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="City name must not contain any special characters.",
            ),
        ],
    )

    tournament_date = DateField(
        "Tournament Date", format="%Y-%m-%d", validators=[DataRequired()]
    )

    submit = SubmitField("Submit")


class RequiredIf(object):
    def __init__(self, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        current_value = form.data.get(field.name)
        if current_value == "None":
            for condition_field, reserved_value in self.conditions.items():
                dependent_value = form.data.get(condition_field)
                if condition_field not in form.data:
                    continue
                elif dependent_value == reserved_value:
                    raise Exception(
                        'Invalid value of field "%s". Field is required when %s==%s'
                        % (field.name, condition_field, dependent_value)
                    )


class Search(FlaskForm):
    """
    A search system to filter tournaments by name and date.
    """

    date = BooleanField("Date:")
    name = BooleanField("Name:")
    start_date = DateField(
        "Start Date:", format="%Y-%m-%d", validators=[RequiredIf(date=True)]
    )
    end_date = DateField(
        "End Date:", format="%Y-%m-%d", validators=[RequiredIf(date=True)]
    )
    tournament_name = StringField(
        "Tournament Name",
        validators=[
            RequiredIf(name=True),
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="Tournament names never contain any special characters.",
            ),
        ],
    )
    submit = SubmitField("Search")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=12, max=64)]
    )
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Request Password Reset")


class ManualPermissionsForm(FlaskForm):
    userID = IntegerField("User ID")
    prID = IntegerField("permission request ID")
    approve = SubmitField("Approve")
    deny = SubmitField("Deny")
    """
    actions = SelectField("permission actions",
                          coerce=int,
                          choices=[(1, 'approve coach'), (2, 'deny coach'), (3, 'approve admin'), (4, 'deny admin')])
    """
    pr_actions = SelectField(
        "permission request actions",
        coerce=int,
        choices=[(1, "approve pr"), (2, "deny pr")],
    )
    submit = SubmitField("Submit changes")


class RequestPermissionsForm(FlaskForm):
    request_coach = SubmitField("Coach request")
    request_admin = SubmitField("Admin request")


class UserSettingsForm(FlaskForm):
    username = StringField("Username", render_kw={"readonly": True})
    firstname = StringField(
        "First Name*",
        validators=[DataRequired()],
        render_kw={"placeholder": "First Name"},
    )
    lastname = StringField(
        "Last Name*",
        validators=[DataRequired()],
        render_kw={"placeholder": "Last Name"},
    )
    phonenumber = StringField("Phone Number", render_kw={"placeholder": "555-555-5555"})
    address = StringField("Address", render_kw={"placeholder": "123 Fake St."})
    email = StringField("Email*", validators=[Email()])

    submit = SubmitField("Update Settings")


class TournamentManagementForm(FlaskForm):
    tournament_name = StringField(
        "Tournament Name",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="Tournament name must not contain any special characters.",
            ),
        ],
    )
    tournament_city = StringField(
        "Tournament City",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="City name must not contain any special characters.",
            ),
        ],
    )

    tournament_date = DateField(
        "Tournament Date", format="%Y-%m-%d", validators=[DataRequired()]
    )

    def validate_tournament_league(form, tournament_league):
        league_string = tournament_league
        if League.query.filter_by(league_name=league_string.data).first():
            raise ValidationError(
                "League already exists. Choose existing league or create a unique league."
            )

    add_team = SubmitField("Add Team")
    remove_team = SubmitField("Remove Team")
    submit = SubmitField("Submit")
    # Very basic number validation, checks that there are 10 digits
    def validate_phonenumber(self, field):
        number = field.data
        number = re.sub("\D", "", number)
        print(field.data)
        if len(number) == 10 or len(number) == 0:
            return
        else:
            raise ValidationError("Invalid phone number")


class TeamSettingsForm(FlaskForm):
    teamname = StringField("Team Name", validators=[DataRequired()])
    coach = StringField("Coach", render_kw={"readonly": True})
    leagues = League.query.all()
    league_list = []
    for league in leagues:
        league_list.append((league.id, league.league_name))
    league = SelectField("League", validators=[DataRequired()], choices=league_list)
    submit = SubmitField("Update Settings")

    def validate_team_name(self, field):
        team = Team.query.filter_by(team_name=field.data).first()
        if team is not None:
            raise ValidationError("Team name is already taken.")


class TeamScore(FlaskForm):
    total_score = IntegerField("Total Score")
    total_wins = IntegerField("Total Wins")
    total_losses = IntegerField("Total Losses")
    submit = SubmitField("Submit")
