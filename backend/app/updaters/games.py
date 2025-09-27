from datetime import datetime

from sqlalchemy.exc import IntegrityError
from requests.exceptions import HTTPError

from app import app, db
from app.scrapers import scrape_pbp_boxscore, scrape_schedule, scrape_pbp, scrape_shifts, scrape_appearances_boxscore
from app.models import Game, Event, EventType, Player, Shift, GameImportError, GoalieAppearance, SkaterAppearance
from app.updaters import log_error, ref_types, players

def insert_games(date: datetime) -> list[int]:
    date_string = date.date().strftime("%Y-%m-%d")
    game_dicts = scrape_schedule(date_string)
    game_ids = []

    if len(game_dicts) == 0:
        app.logger.warning(f"No games found on {date_string}")
        return []
    
    for game_dets in game_dicts:
        game = Game(**game_dets)
        try:
            db.session.merge(game)
            app.logger.info(f'Inserted Game {game}')
            game_ids.append(game.id)
        except IntegrityError as e:
            db.session.rollback()
            app.logger.warning(f'Failed to Insert Game {game}')
            log_error(e)

    return game_ids

def insert_appearances(gameID: int):
    try:
        skater_appearances, goalie_appearances = scrape_appearances_boxscore(gameID)
    except HTTPError as e:
        app.logger.warning(f'Boxscores not found for Game {gameID}')
        app.logger.error(e)
        db.session.add(GameImportError(gameID, "BOX"))
        db.session.commit()
        return
    
    skater_appearances_obj = [SkaterAppearance(**appearance) for appearance in skater_appearances]
    goalie_appearances_obj = [GoalieAppearance(**appearance) for appearance in goalie_appearances]

    try:
        for appearance in skater_appearances_obj:
            db.session.merge(appearance)
        db.session.commit()
        app.logger.info(f'Skater Appearances Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert Skater Appearances for Game {gameID}')
        log_error(e)

    try:
        for appearance in goalie_appearances_obj:
            db.session.merge(appearance)
        db.session.commit()
        app.logger.info(f'Goalie Appearances Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert Goalie Appearances for Game {gameID}')
        log_error(e)

    # Add new players to database
    existing_player_ids = set(player.id for player in Player.query.all())
    new_player_ids = set(appearance.playerID for appearance in skater_appearances_obj + goalie_appearances_obj) - existing_player_ids
    for id in new_player_ids:
        players.insert_or_update_player(id)

def insert_events(gameID: int, insert_new_event_codes=True):
    try:
        plays = scrape_pbp(gameID)
    except HTTPError as e:
        app.logger.warning(f'Events not found for Game {gameID}')
        app.logger.error(e)
        app.logger.info(f'Trying pbp with boxscores for Game {gameID}')
        db.session.add(GameImportError(gameID, "PBP"))
        db.session.commit()
        try:
            plays = scrape_pbp_boxscore(gameID)
        except HTTPError as box_e:
            app.logger.warning(f'Boxscore not found for Game {gameID}')
            app.logger.error(box_e)
            db.session.add(GameImportError(gameID, "BOX"))
            db.session.commit()
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
        db.session.add(GameImportError(gameID, "SHIFTS"))
        db.session.commit()
        return
    
    shift_objs = []

    if len(shifts) == 0:
        app.logger.warning(f'No shift data for Game {gameID}')
        db.session.add(GameImportError(gameID, "SHIFTS"))
        db.session.commit()
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

def delete_goalie_appearances(gameID = None):
    if gameID is not None:
        GoalieAppearance.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted goalie appearances for Game {gameID}')
    else:
        GoalieAppearance.query.delete()
        app.logger.info('Deleted ALL Goalie Appearances')
    db.session.commit()

def delete_skater_appearances(gameID = None):
    if gameID is not None:
        SkaterAppearance.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted skater appearances for Game {gameID}')
    else:
        GoalieAppearance.query.delete()
        app.logger.info('Deleted ALL Skater Appearances')
    db.session.commit()

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