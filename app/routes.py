from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import (
    LoginForm,
    RegistrationForm,
    TournamentCreationForm,
    RequestPermissionForm,
    ManualPermissionsForm
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from app.models import Tournament, User
from werkzeug.urls import url_parse
from app.permissions import *


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


@app.route("/TeamCreation")
def TeamCreation():

    return render_template("TeamCreation.html", title="Team Creation")


@app.route("/TournamentCreation", methods=["GET", "POST"])
def TournamentCreation():
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
        "TournamentCreation.html", title="Tournament Creation", form=form
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

@app.route("/manualPermissions", methods=["GET", "POST"])
def manualPermissions():
    form = ManualPermissionsForm()
    users = db.session.query(User).order_by('id')
    tval = "none"
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.userID.data).first()
        tval = user
        if form.actions.data == '1':
            approve_coach(current_user, user)
        if form.actions.data == '2':
            deny_coach(current_user, user)
        if form.actions.data == '3':
            approve_admin(current_user, user)
        if form.actions.data == '4':
            deny_admin(current_user, user)
    return render_template("ManualPermissions.html", title="Permissions", form=form, users=users, tval=tval)

@app.route("/dbtest", methods=["GET", "POST"])
def dbtest():
    form = RequestPermissionForm()
    users = db.session.query(User).all()
    tval = "none"
    if form.validate_on_submit():
        if form.request_coach.data:
            approve_coach(current_user, current_user)
        elif form.remove_coach.data:
            deny_coach(current_user, current_user)
        if form.request_admin.data:
            approve_admin(current_user, current_user)
        elif form.remove_admin.data:
            deny_admin(current_user, current_user)
        #db.session.commit()
    return render_template("dbtest.html", title="db tests", form=form, users=users, tval=tval)




"""This view function is actually pretty simple, it just returns a greeting as a string. The two strange @app.route 
lines above the function are decorators, a unique feature of the Python language. A decorator modifies the function 
that follows it. A common pattern with decorators is to use them to register functions as callbacks for certain 
events. In this case, the @app.route decorator creates an association between the URL given as an argument and the 
function. In this example there are two decorators, which associate the URLs / and /index to this function. This 
means that when a web browser requests either of these two URLs, Flask is going to invoke this function and pass the 
return value of it back to the browser as a response. If this does not make complete sense yet, it will in a little 
bit when you run this application. """
