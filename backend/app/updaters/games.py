from app import app, db
from app.scrapers import scrape_schedule, scrape_rosters, scrape_pbp, scrape_shifts
from app.models import Game, PlayerGame, Event, EventType, Player, Shift
from app.updaters import log_error, ref_types, players

from sqlalchemy.exc import IntegrityError
from requests.exceptions import HTTPError
from datetime import datetime

def insert_games(date: datetime) -> list[int]:
    date_string = date.date().strftime("%Y-%m-%d")
    game_dicts = scrape_schedule(date_string)
    game_ids = []

    if len(game_dicts) == 0:
        app.logger.warning(f"No games found on {date_string}")
        return []
    
    for game_dets in game_dicts:
        game = Game()
        game.from_dict(game_dets)
        try:
            db.session.merge(game)
            app.logger.info(f'Inserted Game {game}')
            game_ids.append(game.id)
        except IntegrityError as e:
            db.session.rollback()
            app.logger.warning(f'Failed to Insert Game {game}')
            log_error(e)

    return game_ids

def insert_rosters(gameID: int, insert_new_players=True):
    try:
        player_games = scrape_rosters(gameID)
    except HTTPError as e:
        app.logger.warning(f'Rosters not found for Game {gameID}')
        app.logger.error(e)
        return

    player_game_objs = []

    # Add new players to database
    if insert_new_players:
        existing_player_ids = set(i[0] for i in db.session.query(Player.id).all())
        new_player_ids = set(appearance['playerID'] for appearance in player_games) - existing_player_ids
        for id in new_player_ids:
            players.insert_or_update_player(id)
    
    # Add player appearances
    for appearance in player_games:
        player_game = PlayerGame()
        player_game.from_dict(appearance)
        player_game_objs.append(player_game)

    try:
        db.session.add_all(player_game_objs)
        db.session.commit()
        app.logger.info(f'Rosters Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert rosters for Game {gameID}')
        log_error(e)

def insert_events(gameID: int, insert_new_event_codes=True):
    try:
        plays = scrape_pbp(gameID)
    except HTTPError as e:
        app.logger.warning(f'Events not found for Game {gameID}')
        app.logger.error(e)
        return
    
    play_objs = []

    # Add new event codes if not already in database
    if insert_new_event_codes:
        existing_event_codes = set(i[0] for i in db.session.query(EventType.typeCode).all())
        new_event_codes = set(play['typeCode'] for play in plays) - existing_event_codes
        new_event_tuples = set((play['typeCode'],play['typeDescKey']) for play in plays if play['typeCode'] in new_event_codes)

        for tup in new_event_tuples:
            ref_types.insert_event_type(tup)

    # Insert events
    for event in plays:
        play_obj = Event()
        play_obj.from_dict(event)
        play_objs.append(play_obj)

    try:
        db.session.add_all(play_objs)
        db.session.commit()
        app.logger.info(f'Events Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert events for Game {gameID}')
        log_error(e)

def insert_shifts(gameID: int):
    try:
        shifts = scrape_shifts(gameID)
    except HTTPError as e:
        app.logger.warning(f'Shifts not found for Game {gameID}')
        app.logger.error(e)
        return
    
    shift_objs = []

    if len(shifts) == 0:
        app.logger.warning(f'No shift data for Game {gameID}')
        return

    for shift in shifts:
        shift_obj = Shift()
        shift_obj.from_dict(shift)
        shift_objs.append(shift_obj)

    try:
        db.session.add_all(shift_objs)
        db.session.commit()
        app.logger.info(f'Shifts Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert shifts for Game {gameID}')
        log_error(e)

def delete_all_games():
    Game.query.delete()
    db.session.commit()
    app.logger.info('Deleted ALL Games')

def delete_all_player_games():
    PlayerGame.query.delete()
    db.session.commit()
    app.logger.info('Deleted ALL Appearances')

def delete_all_events(gameID = None):
    if gameID is not None:
        Event.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted events for Game {gameID}')
    else:
        Event.query.delete()
        app.logger.info('Deleted ALL Events')
    db.session.commit()

def delete_all_shifts(gameID = None):
    if gameID is not None:
        Shift.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted shifts for Game {gameID}')
    else:
        Shift.query.delete()
        app.logger.info('Deleted ALL Shifts')
    db.session.commit()