from sqlite3 import IntegrityError
from app import app, db
from app.updaters import games, log_error, players, ref_types, teams
from app.models import Game, Event, PlayerGame, Shift, GameImportError

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
import os

def initialise_db():
    app.logger.info('INITIALISING DATABASE')
    teams.insert_teams()
    ref_types.insert_game_types()
    init_player_stats_view()

def init_player_stats_view():
    app.logger.info('CREATING PLAYER STATS VIEW')

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sql', 'season_stats.sql')) as f:
        definition = text(f.read())

    db.session.execute(definition)

def drop_player_stats_view():
    app.logger.info('DROPPING PLAYER STATS VIEW')
    db.session.execute(text("DROP VIEW IF EXISTS 'season_stats'"))

def clear_db(complete=False):
    app.logger.info('CLEARING DATABASE')
    games.delete_all_events()
    games.delete_all_games()
    games.delete_all_player_games()
    games.delete_all_shifts()
    
    if complete:
        players.delete_all_players()
        teams.delete_all_teams()
        ref_types.delete_all_event_types()
        ref_types.delete_all_game_types()

def import_games_on_date(date: datetime):
    app.logger.info(f'IMPORTING GAMES FOR {datetime.strftime(date, '%Y-%m-%d')}')
    game_ids = games.insert_games(date)
    for game_id in game_ids:
        games.insert_rosters(game_id)
        games.insert_events(game_id)
        games.insert_shifts(game_id)

def import_last_gameday():
    import_games_on_date(datetime.today() - timedelta(days = 1))

def import_games_date_range(start: datetime, end: datetime):
    date = start
    while date <= end:
        import_games_on_date(date)
        date += timedelta(days=1)

def remove_game(id: int):
    try:
        game = Game.query.filter_by(id=id).first()
        Event.query.filter_by(gameID=id).delete()
        PlayerGame.query.filter_by(gameID=id).delete()
        Shift.query.filter_by(gameID=id).delete()
        Game.query.filter_by(id=id).delete()
        app.logger.info(f"Removed Events, Rosters, Shifts and Game Info for {game}")
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
        games.delete_all_events(gameID)
        games.delete_all_player_games(gameID)
        games.delete_all_shifts(gameID)
        games.insert_rosters(gameID)
        games.insert_events(gameID)
        games.insert_shifts(gameID)

if __name__ == "__main__":
    app.app_context().push()
    import_games_date_range(datetime(2025, 4, 1), datetime(2025, 4, 17))
    # 23-24 season done
    # 24-25 season done
