from sqlite3 import IntegrityError
from app import app, db
from app.updaters import games, log_error, players, ref_types, teams
from app.models import Game, Event, GoalieAppearance, Player, PlayerGame, Shift, GameImportError

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
import os

def initialise_db():
    app.logger.info('INITIALISING DATABASE')
    teams.insert_teams()
    ref_types.insert_game_types()

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
        games.insert_goalie_appearances(game_id)
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
        GoalieAppearance.query.filter_by(gameID=id).delete()
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
        games.delete_all_goalie_appearances(gameID)
        games.insert_rosters(gameID)
        games.insert_events(gameID)
        games.insert_shifts(gameID)
        games.insert_goalie_appearances(gameID)

def update_all_players():
    ids = [player.id for player in Player.query.all()]
    for id in ids:
        players.insert_or_update_player(id)

if __name__ == "__main__":
    app.app_context().push()
    ids = [game.id for game in Game.query.all()]
    for id in ids:
        games.insert_goalie_appearances(id)
    # 20-21 REG + POST season done
    # 21-22 REG + POST season done
    # 22-23 REG + POST season done
    # 23-24 REG + POST season done
    # 24-25 REG + post season done
    # Need to update players for awards & download postseason data
