from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import (
    LoginForm,
    RegistrationForm,
    TournamentCreationForm,
    TeamCreationForm,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from app.models import Tournament, User, Team
from werkzeug.urls import url_parse


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/dbtest")
def dbtest():

    return redirect(url_for("dbtest"))


@app.route("/tournament_creation", methods=["GET", "POST"])
def tournament_creation():
    form = TournamentCreationForm()
    if form.validate_on_submit():
        tournament = Tournament(
            tournamentName=form.tournamentName.data,
            tournamentDate=form.tournamentDate.data,
            tournamentLocation=form.tournamentLocation.data,
        )
        db.session.add(tournament)
        db.session.commit()
        flash("Congratulations, you have created a tournament!")
        return redirect(url_for("index"))
    return render_template(
        "tournament_creation.html", title="Tournament Creation", form=form
    )


@app.route("/TournamentDashboard")
def TournamentDashboard():
    return render_template("TournamentDashboard.html", title="Tournament Dashboard")


@app.route("/TournamentPage")
def TournamentPage():
    return render_template("TournamentPage.html", title="Tournament Page")


@app.route("/team/<team_ID>", methods=["GET"])
# @login_required
def team(team_ID: int):
    # team = get_team_by_id(team_ID)
    return render_template("teamInfo.html", title="Team Details", team=None)


@app.route("/match/<match_ID>", methods=["GET"])
def match(match_ID: int):
    return render_template("match.html")


@app.route("/league", methods=["GET"])
def league():
    return render_template("league.html")


@app.route("/create_team", methods=["GET", "POST"])
@login_required  # TODO: It would be nice to have coach_required and admin_required decorators for these pages.
def create_team():
    form = TeamCreationForm()
    if form.validate_on_submit():
        team = Team(
            team_name=form.team_name.data, user_is_coach=form.user_is_coach.data
        )
        db.session.add(team)
        db.session.commit()
        flash("Congratulations, you have registered a new team!")
        # TODO: have this redirect to the new team page once it's implemented
        return redirect(url_for("index"))
    return render_template("team_creation.html", title="Register a New Team", form=form)
