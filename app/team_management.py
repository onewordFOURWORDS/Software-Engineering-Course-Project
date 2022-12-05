from app.models import Team, League, Tournament


def get_teams_in_league(league_id: int) -> list[Team]:
    """
    Returns a list of all teams in a given league.
    """
    return Team.query.filter_by(league=league_id).all()


def get_team_by_id(team_id: int) -> Team:
    return Team.query.filter_by(id=team_id).first()
