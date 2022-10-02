from ctypes import addressof
import email
from tokenize import String
from flask import Flask
import datetime

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Welcome to SSBM!</h1><h3>Created by Max, David, Scott, Tim, and Nick</h3>"

<<<<<<< HEAD

class User:
    def __init__(self, userEmail: str, hashedPassword: str, teamsToFollow, firstName: str, lastName: str,
                 address: str, phoneNumber: str):
        self.email = userEmail
        self.hashedPassword = hashedPassword
        self.teamsToFollow = teamsToFollow
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.phoneNumber = phoneNumber


class Coach(User):
    def __init__(self, teamsToFollow, userEmail: str, hashedPassword: str, firstName: str, lastName: str, address: str,
                 phoneNumber: str):
        super().__init__(userEmail, hashedPassword, teamsToFollow, firstName, lastName, address, phoneNumber)
        self.teamsToFollow = teamsToFollow


class Admin(User):
    def __init__(self, teamsToFollow, userEmail: str, hashedPassword: str, firstName: str, lastName: str, address: str,
                 phoneNumber: str):
        super().__init__(userEmail, hashedPassword, teamsToFollow, firstName, lastName, address, phoneNumber)
        self.teamsToFollow = teamsToFollow


class Match:
    def __init__(self, teamOne, teamTwo, teamOneScore: int, teamTwoScore: int):
        self.teamOne = teamOne
        self.teamTwo = teamTwo
        self.teamOneScore = teamOneScore
        self.teamTwoScore = teamTwoScore


class Team:
    def __init__(self, teamName: str, headCoach: Coach, division, totalScore: int, totalScoreAgainst: int,
                 totalWins: int, totalLosses: int, tournaments):
        self.teamName = teamName
        self.headCoach = headCoach
        self.division = division
        self.totalScore = totalScore
        self.totalScoreAgainst = totalScoreAgainst
        self.totalWins = totalWins
        self.totalLosses = totalLosses
        self.tournaments = tournaments


class Tournament:
    def __init__(self, date: datetime.date, location: str, division, tournamentWinner: Team,
                 registeredTeams: [Team]):
        self.date = date
        self.location = location
        self.division = division
        self.tournamentWinner = tournamentWinner
        self.registeredTeams = registeredTeams


class Division:
    def __init__(self, name: str):
        self.name = name
=======
# class User:
#     def __init__(self, email: str, hashedPassword: str, teamsToFollow: [Team], firstName: str, lastName:str,
#         address: str, phoneNumber: str):
#         self.email = email
#         self.hashedPassword = hashedPassword
#         self.teamsToFollow = teamsToFollow
#         self.firstName = firstName
#         self.lastName = lastName
#         self.address = address
#         self.phoneNumber = phoneNumber

# class Coach (User):
#     def __init__(self, teamsToFollow:[Team]):
#         self.teamsToFollow = teamsToFollow

# class Admin (User):
#     def __init__(self, teamsToFollow:[Team]):
#         self.teamsToFollow = teamsToFollow

# class Match:
#     def __init__(self, teamOne: Team, teamTwo: Team, teamOneScore: int, teamTwoScore: int  ):
#         self.teamOne = teamOne
#         self.teamTwo = teamTwo
#         self.teamOneScore = teamOneScore
#         self.teamTwoScore = teamTwoScore

# class Team:
#     def __init__(self, teamName: str, headCoach: Coach, division: Division, totalScore: int, totalScoreAgainst: int,
#         totalWins: int, totalLosses: int, tournaments: [Tournament] ):
#         self.teamName = teamName
#         self.headCoach = headCoach
#         self.division = division
#         self.totalScore = totalScore
#         self.totalScoreAgainst = totalScoreAgainst
#         self.totalWins = totalWins
#         self.totalLosses = totalLosses
#         self.tournaments = tournaments

# class Tournament:
#     def __init__(self, date: datetime.date, location: str, division: Division, tournamentWinner: Team,
#                  registeredTeams: [Team]):
#         self.date = date
#         self.location = location
#         self.division = division
#         self.tournamentWinner = tournamentWinner
#         self.registeredTeams = registeredTeams

# class Division:
#     def __init__(self, name: str):
#         self.name = name

>>>>>>> b60865b (test)
