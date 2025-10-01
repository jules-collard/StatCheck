from datetime import datetime, timedelta
import os
import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from app import app, db
from app.updaters import games, log_error, players, ref_types, teams, events, shifts, appearances
from app.models import Game, Player, GameImportError

def initialise_db():
    app.logger.info('INITIALISING DATABASE')
    teams.insert_teams()
    ref_types.insert_game_types()

def clear_db(complete=False):
    app.logger.info('CLEARING DATABASE')
    events.delete_events()
    appearances.delete_appearances()
    games.delete_games()
    shifts.delete_shifts()
    
    if complete:
        players.delete_all_players()
        teams.delete_all_teams()
        ref_types.delete_all_event_types()
        ref_types.delete_all_game_types()

def import_game(id: int):
    appearances.insert_appearances(id)
    events.insert_events(id)
    shifts.insert_shifts(id)

def import_games_on_date(date: datetime):
    app.logger.info(f'IMPORTING GAMES FOR {datetime.strftime(date, '%Y-%m-%d')}')
    game_ids = games.insert_games(date)
    for game_id in game_ids:
        import_game(game_id)

def import_last_gameday():
    import_games_on_date(datetime.today() - timedelta(days = 1))

def import_games_date_range(start: datetime, end: datetime):
    date = start
    while date <= end:
        import_games_on_date(date)
        date += timedelta(days=1)

def remove_game(id: int):
    try:
        events.delete_events(id)
        shifts.delete_shifts(id)
        appearances.delete_appearances(id)
        games.delete_games(id)
        app.logger.info(f"Removed Events, Rosters, Shifts and Game Info for Game {id}")
        db.session.commit()
    except IntegrityError as e:
        app.logger.warning(f"Failed to Remove Game {id}")
        log_error(e)

def remove_games_after_date(start: datetime):
    games: list[Game] = Game.query.filter(Game.startTimeUTC >= start).all()
    for game in games:
        remove_game(game.id)

def update_games():
    ids = [game.gameID for game in GameImportError.query.all()]
    for gameID in ids:
        GameImportError.query.filter_by(gameID=gameID).delete()
        remove_game(gameID)
        import_game(gameID)

def update_skater_records(gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sql', 'skater_season_records.sql'), 'r') as f:
        skater_query = f.read()

    skater_query_result = db.session.execute(text(skater_query), {"gameType": gameType}).mappings().all()
    results = [dict(row) for row in skater_query_result]

    with open(os.path.join(os.path.dirname(__file__), 'records', f'skater_records_{gameType}.json'), 'w') as f:
        json.dump(results, f)

def update_goalie_records(gameType: int):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sql', 'goalie_season_records.sql'), 'r') as f:
        goalie_query = f.read()

    goalie_query_result = db.session.execute(text(goalie_query), {"gameType": gameType}).mappings().all()
    results = [dict(row) for row in goalie_query_result]

    with open(os.path.join(os.path.dirname(__file__), 'records', f'goalie_records_{gameType}.json'), 'w') as f:
        json.dump(results, f)

def update_max_games():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sql', 'max_games.sql'), 'r') as f:
        query = f.read()

    query_result = db.session.execute(text(query)).mappings().all()
    max_games = [dict(row) for row in query_result]

    with open(os.path.join(os.path.dirname(__file__), 'records', 'max_games.json'), 'w') as f:
        json.dump(max_games, f)

def update_all_records():
    update_skater_records(2)
    update_skater_records(3)
    update_goalie_records(2)
    update_goalie_records(3)

if __name__ == "__main__":
    app.app_context().push()

    update_max_games()
    # 10-11 REG + POST season done
    # 11-12 REG + POST season done
    # 12-13 REG + POST season done
    # 13-14 REG + POST season done
    # 14-15 REG + POST season done
    # 15-16 REG + POST season done
    # 16-17 REG + POST season done
    # 17-18 REG + POST season done
    # 18-19 REG + POST season done
    # 19-20 REG + POST season done
    # 20-21 REG + POST season done
    # 21-22 REG + POST season done
    # 22-23 REG + POST season done
    # 23-24 REG + POST season done
    # 24-25 REG + post season done
