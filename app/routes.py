from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, TournamentCreationForm
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)  # dont worry if pycharm gives a warning here
from app.models import Tournament, User, League
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
@login_required
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


@app.route("/TeamCreation")
def TeamCreation():

    return redirect(url_for("TeamCreation"))


@app.route("/TournamentCreation", methods=["GET", "POST"])
def TournamentCreation():
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
            leagueString = request.form['league']
            league = League.query.filter_by(leagueName=leagueString).first()
        # If the league box is blank, we will take whichever league was selected from the dropdown for the 
        # tournament tournament league, otherwise this function will create a new league based off of the 
        # name they put in and assign the tournament to that league. 
        if form.tournamentLeague.data == '':
            tournament = Tournament(
            tournamentName=form.tournamentName.data,
            tournamentDate=form.tournamentDate.data,
            tournamentLocation=form.tournamentLocation.data,
            tournamentLeague = league.id
        )
            db.session.add(tournament)
            db.session.commit()
        else:
            league = League(
                leagueName = form.tournamentLeague.data,
            )
            db.session.add(league)
            db.session.commit()
            tournament = Tournament(
                tournamentName=form.tournamentName.data,
                tournamentDate=form.tournamentDate.data,
                tournamentLocation=form.tournamentLocation.data,
                tournamentLeague = league.id
            )
            db.session.add(tournament)
            db.session.commit()
        flash("Congratulations, you have created a tournament!")
        return redirect(url_for('TournamentPage', tournament=tournament.tournamentName))
    return render_template(
        "TournamentCreation.html", title="Tournament Creation", form=form, leagues = leagues
    )
    return redirect(url_for("TournamentCreation"))


@app.route("/TournamentDashboard")
def TournamentDashboard():
    tournaments = Tournament.query.all()
    leagues = League.query.all()
    return render_template("TournamentDashboard.html", title="Tournament Dashboard", tournaments = tournaments, leagues = leagues)


@app.route("/TournamentPage",)
def TournamentPage():
    tournamentString = request.args.get('tournament', None)
    tournament = Tournament.query.filter_by(tournamentName=tournamentString).first()
    leagueID = tournament.tournamentLeague
    league = League.query.filter_by(id=leagueID).first()
    return render_template("TournamentPage.html", title="Tournament Page", tournament = tournament, league = league)


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


"""This view function is actually pretty simple, it just returns a greeting as a string. The two strange @app.route 
lines above the function are decorators, a unique feature of the Python language. A decorator modifies the function 
that follows it. A common pattern with decorators is to use them to register functions as callbacks for certain 
events. In this case, the @app.route decorator creates an association between the URL given as an argument and the 
function. In this example there are two decorators, which associate the URLs / and /index to this function. This 
means that when a web browser requests either of these two URLs, Flask is going to invoke this function and pass the 
return value of it back to the browser as a response. If this does not make complete sense yet, it will in a little 
bit when you run this application. """
