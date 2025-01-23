from operator import and_
from sqlite3 import IntegrityError
from app import app, db
from app.updaters import games, log_error, players, ref_types, teams, logger
from app.models import Game, Event, PlayerGame, Shift

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_

def initialise_db():
    logger.info('INITIALISING DATABASE')
    teams.insert_teams()
    ref_types.insert_game_types()

def clear_db():
    logger.warning('CLEARING DATABASE')
    games.delete_all_events()
    games.delete_all_games()
    games.delete_all_player_games()
    games.delete_all_shifts()
    players.delete_all_players()
    teams.delete_all_teams()
    ref_types.delete_all_event_types()
    ref_types.delete_all_game_types()

def import_games_on_date(date: datetime):
    logger.info(f'IMPORTING GAMES FOR {datetime.strftime(date, '%Y-%m-%d')}')
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
        logger.info(f"Removed Events, Rosters, Shifts and Game Info for {game}")
        db.session.commit()
    except IntegrityError as e:
        logger.error(f"Failed to Remove Game {id}")
        log_error(e)

def remove_games_date_range(start: datetime, end: datetime):
    games: list[Game] = Game.query.filter(and_(Game.startTimeUTC >= start, Game.startTimeUTC <= end)).all()
    for game in games:
        remove_game(game.id)


if __name__ == "__main__":
    app.app_context().push()
    start_date = datetime.strptime("2025-01-01", '%Y-%m-%d')
    end_date = datetime.strptime("2025-01-02", '%Y-%m-%d')
    remove_games_date_range(start_date, end_date)
