from sqlalchemy.orm import column_property
from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    full_name = column_property(first_name + " " + last_name)
    address = db.Column(db.String(140))
    phone_number = db.Column(db.String(64))
    affiliated_team = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    # TODO: Change this later: Currently setting _is_coach to be true by default so I can test some of my
    # team management stuff. Also, think about better names for these, just using the leading underscore
    # to avoid collision with the is_admin() and is_coach() methods, which I created to call within Jinja
    # templates even though they are a bit unpythonic. Can I just check the values of these props from
    # within the templates instead of registering the functions?
    # Look into this later, for now, it works...
    _is_admin = db.Column(db.Boolean, default=False)
    _is_coach = db.Column(db.Boolean, default=True)

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

    # Having these be instance methods on Users makes it easy to use these within
    # Jinja.
    def is_admin(self):
        return self._is_admin

    def is_coach(self):
        # print(self)
        return self._is_coach


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
    # totalScore = db.Column(db.Integer)
    # totalScoreAgainst = db.Column(db.Integer)
    # totalWins = db.Column(db.Integer)
    # totalLosses = db.Column(db.Integer)
    # tournaments = db.Column(db.Integer)

    def __repr__(self):
        return "<Team {}>".format(self.teamName)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournamentName = db.Column(db.String(140), index=True, unique=True)
    tournamentDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tournamentLocation = db.Column(db.String(200))
    tournamentLeague = db.Column(db.Integer, db.ForeignKey("league.id"))

    def __repr__(self):
        return "<Tournament {}>".format(self.tournamentName)
