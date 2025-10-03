from app import app
from app.inserters import games, players, ref_types, teams, events, shifts, appearances
from app.analytics.on_ice.updating import delete_split_shifts

def initialise_db():
    app.logger.info('INITIALISING DATABASE')
    teams.insert_teams()
    ref_types.insert_game_types()
    ref_types.insert_event_types()

def clear_db(complete=False):
    app.logger.info('CLEARING DATABASE')
    events.delete_events()
    appearances.delete_appearances()
    games.delete_games()
    shifts.delete_shifts()
    delete_split_shifts()
    
    if complete:
        players.delete_all_players()
        teams.delete_all_teams()
        ref_types.delete_all_event_types()
        ref_types.delete_all_game_types()