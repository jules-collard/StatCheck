from app import app
from app.updaters import games, players, ref_types, teams, logger

from datetime import datetime, timedelta

def initialise_db():
    logger.info('INITIALISING DATABASE')
    teams.insert_teams()
    ref_types.insert_game_types()

def clear_db():
    games.delete_all_events()
    games.delete_all_games()
    games.delete_all_player_games()
    players.delete_all_players()
    teams.delete_all_teams()
    ref_types.delete_all_event_types()
    ref_types.delete_all_game_types()

if __name__ == "__main__":
    app.app_context().push()
    # Commands HERE
    day = datetime.today() - timedelta(days=2)
    games.insert_events(2024020705)
