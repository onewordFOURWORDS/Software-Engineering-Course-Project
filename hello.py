from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Welcome to SSBM!</h1><h3>Created by Max, David, Scott, Tim ...</h3>"