from datetime import datetime, timedelta

from app import app, db
from app.models import GameImportError
from app.inserters import games, appearances, events, shifts
from app.analytics.on_ice.updating import insert_split_shifts, delete_split_shifts
from app.analytics.expected_goals.updating import insert_xg

def import_game(id: int, calc_xg = False):
    appearances.insert_appearances(id)
    events.insert_events(id)
    shifts.insert_shifts(id)
    insert_split_shifts(id)
    if calc_xg:
        insert_xg(id)

def remove_game(id: int):
    events.delete_events(id)
    shifts.delete_shifts(id)
    appearances.delete_appearances(id)
    delete_split_shifts(id)
    games.delete_games(id)
    app.logger.info(f"Removed Events, Rosters, Shifts and Game Info for Game {id}")
    db.session.commit()

def import_games_on_date(datestring: str):
    date = datetime.strptime(datestring, '%Y-%m-%d')
    app.logger.info(f'IMPORTING GAMES FOR {datestring}')
    game_ids = games.insert_games(date)
    for game_id in game_ids:
        import_game(game_id)
    if len(game_ids) > 0:
        insert_xg(*game_ids)

def import_games_date_range(start_string: str, end_string: str):
    date = datetime.strptime(start_string, '%Y-%m-%d')
    end = datetime.strptime(end_string, '%Y-%m-%d')
    while date <= end:
        import_games_on_date(date)
        date += timedelta(days=1)

def import_games_from_errors():
    ids = [game.gameID for game in GameImportError.query.all()]
    for gameID in ids:
        remove_game(gameID)
        GameImportError.query.filter_by(gameID=gameID).delete()
        import_game(gameID)
