from datetime import datetime
from flask_login import UserMixin
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login

"""
classes are defined by extending the db.model class. this allows for db management through flask-sqlalchemy. 
the resulting db is testable in shell and saved to a local file, no need for hosting
"""

following = db.Table(
    "following",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("team.id")),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(128), default="password")
    # teamsToFollow = db.Column(db.Column)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    address = db.Column(db.String(140))
    phone_number = db.Column(db.String(64))

    followed = db.relationship(
        "User",
        secondary=following,
        primaryjoin=(following.c.follower_id == id),
        secondaryjoin=(following.c.followed_id == id),
        backref=db.backref("following", lazy="dynamic"),
        lazy="dynamic",
    )

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

    def follow(self, team):
        if not self.is_following(team):
            self.followed.append(team)

    def unfollow(self, team):
        if self.is_following(team):
            self.followed.remove(team)

    def is_following(self, team):
        return self.followed.filter(following.c.following_id == team.id).count() > 0


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leagueName = db.Column(db.String(64))
    teams = db.relationship("Team", backref="teamReference", lazy="dynamic")

    def __repr__(self):
        return "<League {}>".format(self.leagueName)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(140), index=True, unique=True)
    headCoach = db.Column(db.Integer, db.ForeignKey("user.id"))
    league = db.Column(db.Integer, db.ForeignKey("league.id"))
    totalScore = db.Column(db.Integer)
    totalScoreAgainst = db.Column(db.Integer)
    totalWins = db.Column(db.Integer)
    totalLosses = db.Column(db.Integer)
    tournaments = db.Column(db.Integer)

    def __repr__(self):
        return "<Team {}>".format(self.teamName)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournamentName = db.Column(db.String(140), index=True, unique=True)
    tournamentDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tournamentLocation = db.Column(db.String(200))
    tournamentLeague = db.Column(db.Integer, db.ForeignKey("league.id"))
