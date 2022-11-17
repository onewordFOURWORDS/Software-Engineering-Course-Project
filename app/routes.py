from datetime import date
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.email import send_password_reset_email
from app.forms import (
    LoginForm,
    RegistrationForm,
    TournamentCreationForm,
    Search,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    LeaguePageTeamSelectForm,
    TeamCreationForm,
    ManualPermissionsForm,
    dbtestForm,
    RequestPermissionsForm,
    UserSettingsForm,
    TeamSettingsForm,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from app.models import Tournament, User, League, Team, tournament_teams as tournament_teams_object
from werkzeug.urls import url_parse
from app.team_management import get_teams_in_league, get_team_by_id
from app.permissions import *
from app import db


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
        # if form.affiliated_team.data is not None:
        #    user.follow(form.affiliated_team.data)
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
            if not League.query.all() and form.tournament_league.data == "":
                flash("Please create a league for your tournament!")
                return redirect(url_for("tournament_creation"))
            tournament_state = request.form["state"]
            if League.query.all():
                leagueString = request.form["league"]
                league = League.query.filter_by(league_name=leagueString).first()
        # If the league box is blank, we will take whichever league was selected from the dropdown for the
        # tournament tournament league, otherwise this function will create a new league based off of the
        # name they put in and assign the tournament to that league.
        if form.tournament_league.data == "" and League.query.all():
            tournament = Tournament(
                tournament_name=form.tournament_name.data,
                tournament_date=form.tournament_date.data,
                tournament_city=form.tournament_city.data,
                tournament_state=tournament_state,
                tournament_league=league.id,
            )
            db.session.add(tournament)
            db.session.commit()
        else:
            league = League(
                league_name=form.tournament_league.data,
            )
            db.session.add(league)
            db.session.commit()
            tournament = Tournament(
                tournament_name=form.tournament_name.data,
                tournament_date=form.tournament_date.data,
                tournament_city=form.tournament_city.data,
                tournament_state=tournament_state,
                tournament_league=league.id,
            )
            db.session.add(tournament)
            db.session.commit()
        flash("Congratulations, you have created a tournament!")
        return redirect(
            url_for("tournament_page", tournament=tournament.tournament_name)
        )
    return render_template(
        "tournament_creation.html",
        title="Tournament Creation",
        form=form,
        leagues=leagues,
    )


@app.route("/tournament_dashboard", methods=["GET", "POST"])
def tournament_dashboard():
    # TODO: rework the decorator style again by checking all filters and doing one big query instead of trying to make many small ones
    form = Search()
    leagues = League.query.all()
    form.validate_on_submit()
    start = form.start_date.data
    end = form.end_date.data
    name = form.tournament_name.data
    # build query up decorator style to allow precise searching -- NEVERMIND THIS BREAKS EVERYTHING
    tournaments = Tournament.query

    # filter tournaments inclusive from start to end
    if type(start) == date and type(end) == date:
        tournaments = (
            tournaments.filter(Tournament.tournament_date >= start)
            .filter(Tournament.tournament_date <= end)
            .all()
        )
    # kind of fuzzy search on tournament name
    elif type(name) == str:
        tournaments = tournaments.filter(Tournament.tournament_name.contains(name)).all()
    return render_template("tournament_dashboard.html", title="Tournament Dashboard", form = form, tournaments = tournaments, leagues = leagues)     
    

@app.route("/tournament_page", methods=["GET", "POST"])
def tournament_page():
    tournament_string = request.args.get("tournament", None)
    tournament = Tournament.query.filter_by(tournament_name=tournament_string).first()
    league_id = tournament.tournament_league
    league = League.query.filter_by(id=league_id).first()
    all_teams = Team.query.all()
    all_tournament_teams = db.session.query(tournament_teams_object).all()
    tournament_teams = []
    for tourney_team in all_tournament_teams:
        # pull out teams registered to this tournament
        if tourney_team[0] == tournament.tournament_id:
            # need nested for loops to pull out each team's name
            for team in all_teams:
                # if the ids are the same then you have the right team
                if tourney_team[1] == team.id:
                    # build hashtable with necessary values to display on leaderboard
                    item = {"name": team.team_name, "score": tourney_team[2], "wins": tourney_team[3], "losses": tourney_team[4]}
                    tournament_teams.append(item)
    if request.method == "POST":
        # Edit button will take them to tournament management page.
        if request.form.get("edit_button") == "Edit Tournament":
            return redirect(
                url_for("tournament_management", tournament=tournament.tournament_name)
            )
        # Delete button will delete the tournament from the database and then return the the tournament dahsboard.
        # This will also clear the relations from the teams table.
        elif request.form.get("delete_button") == "Delete Tournament":
            tournament.tournament_teams.clear()
            db.session.delete(tournament)
            db.session.commit()
            flash(
                "You have successfully deleted the following tournament: "
                + tournament.tournament_name
            )
            return redirect(url_for("tournament_dashboard"))
        elif request.form.get("register_button") == "Register":
            # Register will take the team the coach has with the same league, and register that team inside of the tournament.
            for team in all_teams:
                if (
                    team.league == tournament.tournament_league
                    and team.coach == current_user.id
                ):
                    tournament.tournament_teams.append(team)
            db.session.commit()
            flash("You have successfully registered for " + tournament.tournament_name)
            return redirect(
                url_for("tournament_page", tournament=tournament.tournament_name)
            )
        # this creates a copy of the list of tournament teams so that the database is not affected - solely for demostration purposes
        elif request.form.get("add_team") == "Add Fake Team":
            copy = []
            for team in tournament_teams:    
                copy.append(team)
            fake_team = {"name": "FAKE TEAM", "score": 7, "wins": 5, "losses": 3}
            copy.append(fake_team)
            tournament_teams=copy
    return render_template(
        "tournament_page.html",
        title="Tournament Page",
        tournament=tournament,
        league=league,
        teams=all_teams,
        tournament_teams=tournament_teams
    )


@app.route("/tournament_management", methods=["GET", "POST"])
def tournament_management():
    # Tournament management essentially does the same thing as the create team, but instead of making new tournament objects,
    # we are just adding on to the current tournament. With the way leagues are right now, I think we might have to remove
    # the option to edit leagues once a tournament is created for simplicity sakes.
    leagues = League.query.all()
    tournament_string = request.args.get("tournament", None)
    tournament = Tournament.query.filter_by(tournament_name=tournament_string).first()
    tournament_league_name = (
        League.query.filter_by(id=tournament.tournament_league).first()
    ).league_name
    tournament_state = tournament.tournament_state
    form = TournamentCreationForm(obj=tournament)

    if form.validate_on_submit():
        if request.method == "POST":
            tournament_state = request.form["state"]
            leagueString = request.form["league_choose"]
            league = League.query.filter_by(league_name=leagueString).first()
        if form.tournament_league.data == "" and League.query.all():
            tournament.tournament_name = form.tournament_name.data
            tournament.tournament_date = form.tournament_date.data
            tournament.tournament_city = form.tournament_city.data
            tournament.tournament_state = tournament_state
            tournament.tournament_league = league.id
            db.session.commit()
        else:
            league = League(
                league_name=form.tournament_league.data,
            )
            db.session.add(league)
            db.session.commit()
            tournament.tournament_name = form.tournament_name.data
            tournament.tournament_date = form.tournament_date.data
            tournament.tournament_city = form.tournament_city.data
            tournament.tournament_state = tournament_state
            tournament.tournament_league = league.id
            db.session.commit()

        db.session.commit()
        flash("Congratulations, you have updated your tournament!")
        return redirect(
            url_for("tournament_page", tournament=tournament.tournament_name)
        )

    return render_template(
        "tournament_management.html",
        title="Tournament Management",
        form=form,
        leagues=leagues,
        tournament_state=tournament_state,
        tournament_league_name=tournament_league_name,
    )


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
    if current_user.league_id is None:
        teams = None
        form = LeaguePageTeamSelectForm()
        # TODO: Resume here. This is never returning true. hmmm...
        # was not returning true
        if request.method == "POST" and form.validate_on_submit():
            user = current_user
            user.affiliated_team = (
                form.affiliated_team.data
            )  # .data is not actually a team object
            # scott: this does not work because flask forms does not appear to be passing objects back through
            # scott: I have this issue in other places as well
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
    coaches = User.query.filter_by(is_coach=True)
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


@app.route("/manual_permissions", methods=["GET", "POST"])
def manual_permissions():
    form = ManualPermissionsForm()
    users = db.session.query(User).order_by("id")
    prs = db.session.query(PermissionRequest).order_by("id")

    tval = prs
    if form.validate_on_submit():
        # user = User.query.filter_by(id=form.userID.data).first()
        pr = PermissionRequest.query.filter_by(id=form.prID.data).first()
        user = User.query.filter_by(id=pr.user).first()
        tval = pr.id

        """
        if form.actions.data == 1:
            approve_coach(current_user, user)
        if form.actions.data == 2:
            deny_coach(current_user, user)
        if form.actions.data == 3:
            approve_admin(current_user, user)
        if form.actions.data == 4:
            deny_admin(current_user, user)
        """

        if form.pr_actions.data == 1:
            if pr.coach_request == 1:
                approve_coach(current_user, user, pr)
            elif pr.admin_request == 1:
                approve_admin(current_user, user, pr)
        if form.pr_actions.data == 2:
            if pr.coach_request == 1:
                deny_coach(current_user, user, pr)
            elif pr.admin_request == 1:
                deny_admin(current_user, user, pr)

    return render_template(
        "manual_permissions.html",
        title="Permissions",
        form=form,
        users=users,
        prs=prs,
        tval=tval,
    )


@app.route("/request_permission", methods=["GET", "POST"])
def request_permission():
    form = RequestPermissionsForm()
    prs = PermissionRequest.query.filter_by(user=current_user.id).all()
    if form.validate_on_submit():
        if form.actions.data == 1:
            # generate new pr object
            pr = PermissionRequest(coach_request=1, user=current_user.id)
            db.session.add(pr)
            db.session.commit()
        if form.actions.data == 2:
            pr = PermissionRequest(admin_request=1, user=current_user.id)
            db.session.add(pr)
            db.session.commit()
    return render_template(
        "request_permission.html", title="Request Permission", form=form, prs=prs
    )


@app.route("/dbtest", methods=["GET", "POST"])
def dbtest():
    form = dbtestForm()
    users = db.session.query(User).order_by("id")
    teams = db.session.query(Team).order_by("id")
    leagues = db.session.query(League).order_by("id")
    tournaments = db.session.query(Tournament).order_by("id")
    # test value
    tval = "none"
    models = {
        "None": None,
        "User": User,
        "League": League,
        "Team": Team,
        "Tournament": Tournament,
    }
    if form.validate_on_submit():
        clear = models[form.model.data]
        gen = models[form.model_gen.data]
        if clear is not None:
            clear_db(clear)
        if gen is not None:
            gen_db(gen, 10)

    return render_template(
        "dbtest.html",
        title="DB Testing",
        form=form,
        users=users,
        tval=tval,
        teams=teams,
        leagues=leagues,
        tournaments=tournaments,
    )


@app.route("/user_settings", methods=["GET", "POST"])
@login_required
def user_settings():
    form = UserSettingsForm()
    user = current_user
    # user = User.query.get_or_404(current_user.id)

    if request.method == "GET":
        form.username.data = current_user.username
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.address.data = current_user.address
        form.phonenumber.data = current_user.phone_number
        form.email.data = current_user.email

    if form.validate_on_submit():
        # user.username = request.form["username"]
        user.first_name = request.form["firstname"]
        user.last_name = request.form["lastname"]
        # Strips everything but numbers, this can be changed depending
        # on how phone numbers should be stored
        user.phone_number = re.sub("\D", "", request.form["phonenumber"])
        user.address = request.form["address"]
        user.email = request.form["email"]
        try:
            db.session.commit()
            flash("User Information Succesfully Updated!")
            return redirect(url_for("user_settings"))
        except:
            flash("An Error Occured. Please try again!")
            return redirect(url_for("user_settings"))
    return render_template(
        "user_settings.html", form=form, user=user, current_user=current_user
    )


@app.route("/team_settings", methods=["GET", "POST"])
@login_required
def team_settings():
    form = TeamSettingsForm()

    coach_id = current_user.id
    team = Team.query.filter_by(coach=coach_id).first()
    league = League.query.filter_by(id=team.league).first()

    if request.method == "GET":
        form.coach.data = current_user.first_name + " " + current_user.last_name
        form.teamname.data = team.team_name
        # form.league.data = league.league_name

    if form.validate_on_submit():
        try:
            db.session.commit()
            flash("User Information Succesfully Updated!")
            return redirect(url_for("user_settings"))
        except:
            flash("An Error Occured. Please try again!")
            return redirect(url_for("user_settings"))
    return render_template("team_settings.html", form=form)
