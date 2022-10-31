from app import app, db
from app.models import User, League, Team, Tournament, PermissionRequest

# adds db to shell sessions for testing
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "League": League,
        "Team": Team,
        "Tournament": Tournament,
        "PermissionRequest": PermissionRequest
    }
