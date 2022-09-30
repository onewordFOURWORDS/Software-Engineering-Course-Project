from ctypes import addressof
import email
from tokenize import String
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Welcome to SSBM!</h1><h3>Created by Max, David, Scott, Tim, and Nick</h3>"

class Team:
    pass

class User:
    def __init__(self, email: str, hashedPassword: str, teamsToFollow: [Team], firstName: str, lastName:str,
        address: str, phoneNumber: str):
        self.email = email
        self.hashedPassword = hashedPassword
        self.teamsToFollow = teamsToFollow
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.phoneNumber = phoneNumber

class Coach (User):
    def __init__(self, teamsToFollow:[Team]):
        self.teamsToFollow = teamsToFollow

class Admin (User):
    def __init__(self, teamsToFollow:[Team]):
        self.teamsToFollow = teamsToFollow

class Match:
    def __init__(self, teamOne: Team, ):


