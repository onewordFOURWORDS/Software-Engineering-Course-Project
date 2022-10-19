from app.models import Team, League, Tournament
from datetime import datetime

# NOTE: Max here, still unsure how we're going to end up structuring the project in the end. These were all originally conceived
# as class methods, eg myTeam.change_league(new_league) instead of change_league(myTeam, newLeague).
# Keeping these here for now but might reorganize in the future.


def change_league(team: Team, new_league: League):
    """
    Assigns a team to a new league. Used when teams advance in age groups, or move to a new location.
    """
    pass


# def get_upcoming_matches(
#     team: Team, start_time: datetime, end_time: datetime
# ) -> list[Match]:
#     """
#     Gets a list of upcoming matches for a given time that fall between given start and end dates.
#     """
#     pass


# TODO: Define model for match
# def get_finished_matches(
#     team: Team, start_time: datetime = None, end_time: datetime = None
# ) -> list[Match]:
#     """
#     Gets a list of finished matches for a given team. By default, fetches all past matches.
#     Can specify start and end dates to return only matches from a given timeframe.
#     """
#     pass


def add_tournament(team: Team, tournament: Tournament):
    """
    Adds a given tournament to the given teams schedule.
    """
    pass


def remove_tournament(team: Team, tournament: Tournament):
    """
    Removes a tournament from a team's schedule.
    """
    pass


def add_team_to_league(team: Team, league: League):
    """
    Adds the given team to a league.
    """
    pass


def remove_team_from_league(team: Team, league: League):
    """
    Removes the given team from the given league.
    """
    pass


def get_teams_in_league(league_id: int) -> list[Team]:
    """
    Returns a list of all teams in a given league.
    """
    return Team.query.filter_by(league=league_id).all()


def get_team_by_id(team_id: int) -> Team:
    return Team.query.filter_by(id=team_id).first()


def get_stats(team: Team):
    """
    Gets stats for a given team. Need to talk to David about this, I'm not sure what exactly
    he wants to display from my component. As such I've left the return type blank, but it won't be None.
    Thinking we'll have some derived attributes so this will probably involve some work here and not
    just grabbing something from the db.
    """
    pass
