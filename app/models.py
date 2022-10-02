from app import db, login
from datetime import datetime
from flask_login import UserMixin  # dont worry if pycharm gives a warning here
from werkzeug.security import generate_password_hash, check_password_hash

'''
classes are defined by extending the db.model class. this allows for db management through flask-sqlalchemy. 
the resulting db is testable in shell and saved to a local file, no need for hosting
'''

following = db.Table('following',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('team.id'))
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashedPassword = db.Column(db.String(128), default='password')
    #teamsToFollow = db.Column(db.Column)
    firstName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    address = db.Column(db.String(140))
    phoneNumber = db.Column(db.String(64))

    followed = db.relationship(
        'User', secondary=following,
        primaryjoin=(following.c.follower_id == id),
        secondaryjoin=(following.c.followed_id == id),
        backref=db.backref('following', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.hashedPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashedPassword, password)

    def follow(self, team):
        if not self.is_following(team):
            self.followed.append(team)

    def unfollow(self, team):
        if self.is_following(team):
            self.followed.remove(team)

    def is_following(self, team):
        return self.followed.filter(
            following.c.following_id == team.id).count() > 0

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leagueName = db.Column(db.String(64))
    teams = db.relationship('Team', backref='teamReference', lazy='dynamic')

    def __repr__(self):
        return '<League {}>'.format(self.leagueName)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(140), index=True, unique=True)
    headCoach = db.Column(db.Integer, db.ForeignKey('user.id'))
    league = db.Column(db.Integer, db.ForeignKey('league.id'))
    totalScore = db.Column(db.Integer)
    totalScoreAgainst = db.Column(db.Integer)
    totalWins = db.Column(db.Integer)
    totalLosses = db.Column(db.Integer)
    tournaments = db.Column(db.Integer)

    def __repr__(self):
        return '<Team {}>'.format(self.teamName)







