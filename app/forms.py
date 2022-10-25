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
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Regexp,
    Length,
) 
from app.models import User, Tournament, League, Team
from flask_wtf.file import FileField
from datetime import date
from operator import itemgetter


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class TeamCreationForm(FlaskForm):
    team_name = StringField("Team Name", validators=[DataRequired()])
    # TODO: probably write a get_coaches(league) fcn, 2nd time I've done this.
    # waiting on decisions as to how we're handling Leagues.
    coaches = User.query.filter_by(is_coach=True)
    # TODO: Figure out a better way to do this. I want the current user to be the top option.
    # or to have a checkbox "I'm coaching this team" and then show/hide the dropdown with the other options.
    # but I've been fussing with this for ages and it's not working, so just keep going for now as is...
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


# TODO: Figure out nesting forms so this can be reused throughout the site.
# For now just have a separate form for the league page.
# class TeamSelectForm(FlaskForm):
#     class Meta:
#         csrf = False

#     teams = Team.query.all()
#     print("TeamSelectForm is at least being included.")
#     team_list = []
#     for team in teams:
#         team_list.append((team.id, team.team_name))
#     print(team_list)
#     affiliated_team = SelectField(
#         "Choose a team to be affiliated with, or select None to set this up later: ",
#         choices=team_list.sort(),
#         coerce=int,
#     )


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=64)]
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
    )
    # affiliated_team = FieldList(FormField(TeamSelectForm))
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
        # don't include None in this list, doesn't make any sense on this page.
        # this might be an argument for keeping this form as a separate form, but we'll see.
        # TODO: can still factor the team bit out into a get_all_teams or something
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


class TournamentCreationForm(FlaskForm):
    tournamentName = StringField(
        "Tournament Name",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="Tournament name must not contain any special characters.",
            ),
        ],
    )
    tournamentLocation = StringField(
        "Tournament City",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="City name must not contain any special characters.",
            ),
        ],
    )
    tournamentLeague = StringField(
        "Or Create A New League",
        validators=[
            Regexp(
                regex=r"[ \'A-Za-z0-9]*$",
                message="League name must not contain any special characters.",
            )
        ],
        render_kw={
            "placeholder": "Please leave empty if you do not wish to create a league!"
        },
    )
    tournamentDate = DateField(
        "TournamentDate", format="%Y-%m-%d", validators=[DataRequired()]
    )

    def validate_tournamentDate(form, tournamentDate):
        if tournamentDate.data < date.today():
            raise ValidationError("Date must be set in the future.")

    def validate_tournamentLeague(form, tournamentLeague):
        leagueString = tournamentLeague
        if League.query.filter_by(league_name=leagueString.data).first():
            raise ValidationError(
                "League already exists. Choose existing league or create a unique league."
            )

    submit = SubmitField("Create Tournament")


class SearchByDate(FlaskForm):
    """
    A search bar to filter tournaments by date. Leaving end date blank will show all upcoming tournaments.
    """
    startDate = DateField("StartDate", format="%Y-%m-%d", validators=[DataRequired()])
    endDate = DateField("EndDate", format="%Y-%m-%d")
    submit = SubmitField("Search")

    def validate_dates(form, startDate, endDate):
        # if no start date is specified then don't render template showing tournies
        if startDate.data is None:
            return False
        # if this statement is reached then there is a specified start date.
        # if end date is not specified then return true to show all tournies from start date on
        elif endDate.data is None:
            return True
        # if both start and end dates are specified throw an error if the end comes before the start
        # otherwise return true to show all tournies in range of start to end
        elif endDate.data < startDate:
            raise ValidationError("Start date must be before end date.")
        else:
            return True
            

class SearchByDate(FlaskForm):
    """
    A search bar to filter tournaments by date. Leaving end date blank will show all upcoming tournaments.
    """
    startDate = DateField("StartDate", format="%Y-%m-%d", validators=[DataRequired()])
    endDate = DateField("EndDate", format="%Y-%m-%d")
    submit = SubmitField("Search")

    def validate_dates(form, startDate, endDate):
        # if no start date is specified then don't render template showing tournies
        if startDate.data is None:
            return False
        # if this statement is reached then there is a specified start date.
        # if end date is not specified then return true to show all tournies from start date on
        elif endDate.data is None:
            return True
        # if both start and end dates are specified throw an error if the end comes before the start
        # otherwise return true to show all tournies in range of start to end
        elif endDate.data < startDate:
            raise ValidationError("Start date must be before end date.")
        else:
            return True
            

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=64)]
    )
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Request Password Reset")


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

