from app import app, db
from app.updaters import games, players, ref_types, teams, logger
from app.models import Player, Team

from datetime import datetime, timedelta

def initialise_db():
    logger.info('INITIALISING DATABASE')
    teams.insert_teams()
    ref_types.insert_game_types()

def clear_db():
    logger.warning('CLEARING DATABASE')
    games.delete_all_events()
    games.delete_all_games()
    games.delete_all_player_games()
    players.delete_all_players()
    teams.delete_all_teams()
    ref_types.delete_all_event_types()
    ref_types.delete_all_game_types()

def import_games_on_date(date: datetime):
    logger.info(f'IMPORTING GAMES FOR {datetime.strftime(date, '%Y-%m-%d')}')
    game_ids = games.insert_games(date)
    for game in game_ids:
        games.insert_rosters(game)
        games.insert_events(game)

def import_last_gameday():
    import_games_on_date(datetime.today() - timedelta(days = 1))

def import_games_date_range(start: datetime, end: datetime):
    date = start
    while date <= end:
        import_games_on_date(date)
        date += timedelta(days=1)

if __name__ == "__main__":
    app.app_context().push()
