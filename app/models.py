from sqlalchemy.orm import column_property
from datetime import datetime
from flask_login import UserMixin, current_user
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login
import random
import string

"""
classes are defined by extending the db.model class. this allows for db management through flask-sqlalchemy. 
the resulting db is testable in shell and saved to a local file, no need for hosting
"""

# following = db.Table(
#     "following",
#     db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
#     db.Column("followed_id", db.Integer, db.ForeignKey("team.id")),
# )

tournament_teams = db.Table(
    "tournament_teams",
    db.Column("tournament_id", db.Integer, db.ForeignKey("tournament.tournament_id")),
    db.Column("team_id", db.Integer, db.ForeignKey("team.id")),    
    db.Column(("score"), db.Integer),
    db.Column(("wins"), db.Integer),
    db.Column(("losses"), db.Integer)
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
    # TODO: Change this later: Currently setting _is_coach to be true by default so I can test some of my
    # team management stuff. Also, think about better names for these, just using the leading underscore
    # to avoid collision with the is_admin() and is_coach() methods, which I created to call within Jinja
    # templates even though they are a bit unpythonic. Can I just check the values of these props from
    # within the templates instead of registering the functions?
    # Look into this later, for now, it works...

    # using boolean for testing purposes, may create coach and admin subclasses later
    is_admin = db.Column(db.Boolean, default=0)
    is_coach = db.Column(db.Boolean, default=0)
    coach_approve_id = db.Column(db.Integer)
    admin_approve_id = db.Column(db.Integer)
    league_id = db.Column(db.Integer, db.ForeignKey("league.id"), default=None)
    # following relationship, many to many
    #teams = db.relationship('Following', backref='users', cascade="delete")
    """    
    followed = db.relationship(
        "Team",
        secondary=following,
        primaryjoin=(following.c.follower_id == id),
        secondaryjoin=(following.c.followed_id == id),
        backref=db.backref("users", lazy="dynamic"),
        lazy="dynamic",
    )
    """

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

    #def follow(self, team):
    #    if not self.is_following(team):
    #        self.teams.append(team)

    #def unfollow(self, team):
    #    if self.is_following(team):
    #        self.teams.remove(team)

    #def is_following(self, team):
    #    return team in self.teams

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # commented out the following functions, replaced in permissions.py
    # please delete if no longer needed

    # Having these be instance methods on Users makes it easy to use these within
    # Jinja.
    """
    def is_admin(self):
        return self.is_admin

    def is_coach(self):
        # print(self)
        return self.is_coach
"""

    # view league info will likely be done based on a selected league
    # having a dedicated affiliated league for each user may not be helpful,
    # instead a list of followed leagues may be better, similar to the followed teams

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
    # the cascade delete here only impacts the many to many relationship
    #users = db.relationship('Following', backref='teams', cascade="delete")

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
    tournament_league = db.Column(db.Integer, db.ForeignKey("league.id",))
    tournament_teams = db.relationship(
        "Team", secondary=tournament_teams, backref="tournament"
    )

    def __repr__(self):
        return "<Tournament {}>".format(self.tournament_name)


# TODO change the name since following is too generic and users may want to follow leagues
class Following(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='SET NULL'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey(Team.id, ondelete='SET NULL'), primary_key=True)


class PermissionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer,  db.ForeignKey("user.id", ondelete='CASCADE'))
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
            t = Tournament(tournament_name=name, tournament_location=name, tournament_league=league.id)
            db.session.add(t)
            db.session.commit()

