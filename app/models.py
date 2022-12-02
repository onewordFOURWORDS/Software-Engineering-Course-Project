from sqlalchemy.orm import column_property
from datetime import datetime
from flask_login import UserMixin, current_user
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login
import random
import string


tournament_teams = db.Table(
    "tournament_teams",
    db.Column(
        "tournament_id",
        db.Integer,
        db.ForeignKey("tournament.tournament_id"),
        primary_key=True,
    ),
    db.Column("team_id", db.Integer, db.ForeignKey("team.id"), primary_key=True),
    db.Column(("score"), db.Integer),
    db.Column(("wins"), db.Integer),
    db.Column(("losses"), db.Integer),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(128), default="password")
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    full_name = column_property(first_name + " " + last_name)
    address = db.Column(db.String(140))
    phone_number = db.Column(db.String(64))

    affiliated_team = db.Column(db.Integer, db.ForeignKey("team.id"), default=None)
    is_admin = db.Column(db.Boolean, default=0)
    is_coach = db.Column(db.Boolean, default=0)
    coach_approve_id = db.Column(db.Integer)
    admin_approve_id = db.Column(db.Integer)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_reset_password_token(self, expires_in=1200):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            print(
                jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
                    "reset_password"
                ]
            )
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
                "reset_password"
            ]
        except:
            return
        return User.query.get(id)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @property
    def league_id(self):

        # Looks up users affiliated league (based on their team affiliation)

        return Team.query.filter_by(id=self.affiliated_team).first().league


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(64))

    # teams = db.relationship("Team", backref="teamReference", lazy="dynamic")

    def __repr__(self):
        return "<League {}>".format(self.league_name)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(140), index=True, unique=True)
    coach = db.Column(db.Integer, db.ForeignKey("user.id"))
    league = db.Column(db.Integer, db.ForeignKey("league.id"))

    def __repr__(self):
        return "<Team {}>".format(self.team_name)

    @property
    def coach_name(self):
        return User.query.filter_by(id=self.coach).first().full_name

    @property
    def league_name(self):
        return League.query.filter_by(id=self.league).first().league_name


class Tournament(db.Model):
    tournament_id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(140), index=True, unique=True)
    tournament_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tournament_city = db.Column(db.String(200))
    tournament_state = db.Column(db.String(2))
    tournament_league = db.Column(
        db.Integer,
        db.ForeignKey(
            "league.id",
        ),
    )
    tournament_teams = db.relationship(
        "Team", secondary=tournament_teams, backref="tournament"
    )

    def __repr__(self):
        return "<Tournament {}>".format(self.tournament_name)


# TODO change the name since following is too generic and users may want to follow leagues
class Following(db.Model):
    user_id = db.Column(
        db.Integer, db.ForeignKey(User.id, ondelete="SET NULL"), primary_key=True
    )
    team_id = db.Column(
        db.Integer, db.ForeignKey(Team.id, ondelete="SET NULL"), primary_key=True
    )


class PermissionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    username = db.Column(db.String(64))
    label = db.Column(db.String(140))
    coach_request = db.Column(db.Boolean, default=0)
    admin_request = db.Column(db.Boolean, default=0)


def clear_db(model):
    elements = model.query.all()
    for m in elements:
        db.session.delete(m)
    db.session.commit()
    if model == User:
        rebuild_users()
    return


def rebuild_users():
    pw = "pbkdf2:sha256:260000$Q2JJAaHpYOxsdPFx$fc0919f2eb018351b9c55e748ab1f69f2731b560f42e285b625046c45170b70e"
    admin = User(
        username="admin",
        email="support@supersickbracketmaker.tech",
        hashed_password=pw,
        first_name="admin",
        last_name="support",
        is_admin=1,
    )
    Scott = User(
        username="Scott_Gere",
        email="sgman0997@gmail.com",
        hashed_password=pw,
        first_name="Scott",
        last_name="Gere",
        is_admin=1,
        is_coach=1,
    )
    db.session.add_all([admin, Scott])
    db.session.commit()
    return


def gen_db(model, num):
    # must be coach to generate teams
    league = League.query.first()
    if not league:
        league = League(league_name="test league")
        db.session.add(league)
        db.session.commit()
    if model is Team:
        for i in range(num):
            name = "".join(random.choice(string.ascii_letters) for j in range(5))
            t = Team(team_name=name, coach=current_user.id, league=league.id)
            db.session.add(t)
            db.session.commit()
    elif model is League:
        for i in range(num):
            name = "".join(random.choice(string.ascii_letters) for j in range(5))
            l = League(league_name=name)
            db.session.add(l)
            db.session.commit()
    elif model is Tournament:
        for i in range(num):
            name = "".join(random.choice(string.ascii_letters) for j in range(5))
            t = Tournament(
                tournament_name=name, tournament_state="NC", tournament_league=league.id
            )
            db.session.add(t)
            db.session.commit()
