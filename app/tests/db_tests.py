from app.routes import *
from app.models import *

# from _init_

from app.models import *
with app.app_context():
    db.create_all()

# from routes

@app.route("/dbtest", methods=["GET", "POST"])
@login_required
def dbtest():
    # if user not coach or admin, deny access by redirect
    if not (current_user.is_coach or current_user.is_admin):
        return redirect(url_for("access_denied"))
    form = dbtestForm()
    users = db.session.query(User).order_by('id')
    teams = db.session.query(Team).order_by('id')
    leagues = db.session.query(League).order_by('id')
    tournaments = db.session.query(Tournament).order_by('tournament_id')
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


# from models

def clear_db(model):
    elements = model.query.all()
    for m in elements:
        db.session.delete(m)
    db.session.commit()
    if model == User:
        rebuild_users()
    return

# TODO: other dev team members- add your info here and a hashed password if you want one in order to auto generate
def rebuild_users():
    pw = 'pbkdf2:sha256:260000$Q2JJAaHpYOxsdPFx$fc0919f2eb018351b9c55e748ab1f69f2731b560f42e285b625046c45170b70e'
    admin = User(username='admin',
                 email='support@supersickbracketmaker.tech',
                 hashed_password=pw,
                 first_name='admin',
                 last_name='support',
                 is_admin=1
                 )
    Scott = User(username='Scott_Gere',
                 email='sgman0997@gmail.com',
                 hashed_password=pw,
                 first_name='Scott',
                 last_name='Gere',
                 is_admin=1,
                 is_coach=1
                 )
    db.session.add_all([admin, Scott])
    db.session.commit()
    return


def gen_db(model, num):
    # must be coach to generate teams
    league = League.query.first()
    if not league:
        league = League(league_name='test league')
        db.session.add(league)
        db.session.commit()
    if model is Team:
        for i in range(num):
            name = (''.join(random.choice(string.ascii_letters) for j in range(5)))
            t = Team(team_name=name, coach=current_user.id, league=league.id)
            db.session.add(t)
            db.session.commit()
    elif model is League:
        for i in range(num):
            name = (''.join(random.choice(string.ascii_letters) for j in range(5)))
            l = League(league_name=name)
            db.session.add(l)
            db.session.commit()
    elif model is Tournament:
        for i in range(num):
            name = (''.join(random.choice(string.ascii_letters) for j in range(5)))
            t = Tournament(tournament_name=name, tournament_state='NC', tournament_league=league.id)
            db.session.add(t)
            db.session.commit()


user = User.query.filter_by(username='admin').first()
if not user:
    rebuild_users()















