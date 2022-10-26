from datetime import date, datetime
from tracemalloc import start
from xmlrpc.client import DateTime
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.email import send_password_reset_email
from app.forms import (
    LoginForm,
    RegistrationForm,
    TournamentCreationForm,
    SearchByDate,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    LeaguePageTeamSelectForm,
    TeamCreationForm,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from app.models import Tournament, User, League, Team
from werkzeug.urls import url_parse
from wtforms.fields.core import Label
from app.team_management import get_teams_in_league, get_team_by_id


@app.route("/")
@app.route("/index")
def index():
    creators = [
        {"creator": {"username": "Max"}},
        {"creator": {"username": "David"}},
        {"creator": {"username": "Scott"}},
        {"creator": {"username": "Tim"}},
        {"creator": {"username": "Nick"}},
    ]
    return render_template("index.html", title="SSBM!", creators=creators)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            affiliated_team=form.affiliated_team.data,
        )
        user.set_password(form.password.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        # TODO: Upon successful registration, log the user in and take them to the homepage
        # # instead of making them log in manually.
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("login"))
    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("reset_password_request"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("register"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("login"))
    return render_template("reset_password.html", form=form)


@app.route("/dbtest")
def dbtest():

    return redirect(url_for("dbtest"))


@app.route("/tournament_creation", methods=["GET", "POST"])
def tournament_creation():
    """
    If the league box is blank, we will take whichever league was selected from the dropdown for the
    tournament tournament league, otherwise this function will create a new league based off of the
    name they put in and assign the tournament to that league. The tournament is then created based
    off all of the information put in.

    """
    leagues = League.query.all()
    form = TournamentCreationForm()
    if form.validate_on_submit():

        if request.method == "POST":
            # If the database has no current leagus and they do not put one in the box, it will take them back to the page asking
            # to create a league.
            if not League.query.all() and form.tournamentLeague.data == "":
                flash("Please create a league for your tournament!")
                return redirect(url_for("tournament_creation"))
            tournamentState = request.form["state"]
            if League.query.all():
                leagueString = request.form["league"]
                league = League.query.filter_by(league_name=leagueString).first()
        # If the league box is blank, we will take whichever league was selected from the dropdown for the
        # tournament tournament league, otherwise this function will create a new league based off of the
        # name they put in and assign the tournament to that league.
        if form.tournamentLeague.data == "" and League.query.all():
            tournament = Tournament(
                tournamentName=form.tournamentName.data,
                tournamentDate=form.tournamentDate.data,
                tournamentLocation=form.tournamentLocation.data
                + ","
                + " "
                + tournamentState,
                tournamentLeague=league.id,
            )
            db.session.add(tournament)
            db.session.commit()
        else:
            league = League(
                league_name=form.tournamentLeague.data,
            )
            db.session.add(league)
            db.session.commit()
            tournament = Tournament(
                tournamentName=form.tournamentName.data,
                tournamentDate=form.tournamentDate.data,
                tournamentLocation=form.tournamentLocation.data
                + ","
                + " "
                + tournamentState,
                tournamentLeague=league.id,
            )
            db.session.add(tournament)
            db.session.commit()
        flash("Congratulations, you have created a tournament!")
        return redirect(url_for("TournamentPage", tournament=tournament.tournamentName))
    return render_template(
        "tournament_creation.html",
        title="Tournament Creation",
        form=form,
        leagues=leagues,
    )


@app.route("/TournamentDashboard", methods=["GET"])
def TournamentDashboard():
    form = SearchByDate()
    start = request.args.get("startDate") # returns string from GET or None if no query has been made yet - cannot be empty
    end = request.args.get("endDate") # returns string from GET or None if no query has been made yet - can be empty
    # if start is None then no query has been made - do not show any tournaments (return empty list to template)
    if start is None:
        return render_template("TournamentDashboard.html", title="Tournament Dashboard", form = form, tournaments = [])
    # if start is not None end can be an empty string and cannot convert to datetime 
    elif start is not None and end == "":
        start = datetime.strptime(start.strip(), '%Y-%m-%d')
        # show all past and upcoming tournaments inclusive from start
        tournaments = Tournament.query.filter(Tournament.tournamentDate >= start).all()
    # otherwise both dates are valid
    elif start is not None and end != "":
        start = datetime.strptime(start.strip(), '%Y-%m-%d')
        end = datetime.strptime(end.strip(), '%Y-%m-%d')
        # filter tournaments inclusive from start to end
        tournaments = Tournament.query.filter(Tournament.tournamentDate >= start).filter(Tournament.tournamentDate <= end).all()
    return render_template("TournamentDashboard.html", title="Tournament Dashboard", form = form, tournaments = tournaments)


@app.route("/TournamentPage", methods=["GET", "POST"])
def TournamentPage():
    tournamentString = request.args.get("tournament", None)
    tournament = Tournament.query.filter_by(tournamentName=tournamentString).first()
    leagueID = tournament.tournamentLeague
    league = League.query.filter_by(id=leagueID).first()
    if request.method == "POST":
        if request.form["edit_button"]:
            return redirect(url_for('EditTournament', tournament=tournament.tournamentName))
    return render_template("TournamentPage.html", title="Tournament Page", tournament = tournament, league = league)

@app.route("/EditTournament", methods=["GET", "POST"])
def EditTournament():
    form = TournamentCreationForm()
    leagues = League.query.all()
    tournamentString = request.args.get('tournament', None)
    tournament = Tournament.query.filter_by(tournamentName=tournamentString).first()
    form.tournamentName.data = tournament.tournamentName
    form.tournamentDate.data = tournament.tournamentDate
    form.tournamentLocation.data = tournament.tournamentLocation[:-4]
    tournament_state = tournament.tournamentLocation[len(tournament.tournamentLocation)-2:]
    leagueID = tournament.tournamentLeague
    league = League.query.filter_by(id=leagueID).first()
    tournament_league = league.leagueName



    return render_template("EditTournament.html", title="Tournament Management", form=form, leagues = leagues, tournament_state = tournament_state,
    tournament_league = tournament_league )


@app.route("/<team_ID>/team", methods=["GET", "POST"])
# @login_required
def team(team_ID: int):
    team = get_team_by_id(team_ID)
    return render_template("team_info.html", title=team.team_name, team=team)


@app.route("/<match_ID>/match", methods=["GET", "POST"])
def match(match_ID: int):
    return render_template("match.html")


@app.route("/league", methods=["GET", "POST"])
def league():
    # if the user doesn't have an affiliated team and league,
    # the template will display a form so they can select one.
    if current_user.league_id == None:
        teams = None
        form = LeaguePageTeamSelectForm()
        # TODO: Resume here. This is never returning true. hmmm...
        if request.method == "POST" and form.validate_on_submit():
            user = current_user
            user.affiliated_team = form.affiliated_team.data
            db.session.commit()
            return redirect(url_for("league"))
    # otherwise, it will display the teams in their league.
    else:
        form = None
        teams = get_teams_in_league(current_user.league_id)

    return render_template("league.html", teams=teams, form=form)


@app.route("/create_team", methods=["GET", "POST"])
@login_required  # TODO: It would be nice to have coach_required and admin_required decorators for these pages.
def create_team():
    # TODO: Might want to update this later when coach and admin classes are
    # defined/we have a coaches table.
    coaches = User.query.filter_by(_is_coach=True)
    form = TeamCreationForm()
    if form.validate_on_submit():
        team = Team(
            team_name=form.team_name.data,
            coach=form.coach.data,
            league=form.league.data,
        )
        db.session.add(team)
        db.session.commit()
        flash("Congratulations, you have registered a new team!")
        # TODO: have this redirect to the new team page once it's implemented
        return redirect(url_for("index"))
    return render_template(
        "team_creation.html",
        title="Register a New Team",
        form=form,
        coaches=coaches,
        current_user=current_user,
    )
