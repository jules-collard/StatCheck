from app import app, db
from app.scrapers import scrape_schedule, scrape_rosters, scrape_pbp
from app.models import Game, PlayerGame, Event, EventType, Player
from app.updaters import ref_types, players
from app.updaters import logger

from sqlalchemy.exc import IntegrityError
from datetime import datetime

def insert_games(date: datetime):
    date_string = date.date().strftime("%Y-%m-%d")
    logger.info('Inserting Games for %(date_string)s')
    game_dicts = scrape_schedule(date_string)
    game_objects = []

    for game_dets in game_dicts:
        game = Game()
        game.from_dict(game_dets)
        game_objects.append(game)

    try:
        db.session.add_all(game_objects)
        db.session.commit()
        logger.info('Games Inserted for %(date_string)s')
    except IntegrityError as e:
        db.session.rollback()
        logger.error('Failed to insert games for %(date_string)s')
        logger.debug(e.statement)
        logger.debug(e.orig)

def insert_rosters(gameID: int, insert_new_players=True):
    logger.info('Inserting Rosters for Game %(gameID)d')
    player_games = scrape_rosters(gameID)
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
        logger.info('Rosters Inserted for Game %(gameID)d')
    except IntegrityError as e:
        db.session.rollback()
        logger.error('Failed to insert rosters for Game %(gameID)d')
        logger.debug(e.statement)
        logger.debug(e.orig)

def insert_events(gameID: int, insert_new_event_codes=True):
    logger.info('Inserting Events for Game %(gameID)d')
    plays = scrape_pbp(gameID)
    play_objs = []

    # Add new event codes if not already in database
    if insert_new_event_codes:
        existing_event_codes = set(i[0] for i in db.session.query(EventType.typeCode).all())
        new_event_codes = set(play['typeCode'] for play in plays) - existing_event_codes
        new_event_tuples = set((play['typeCode'],play['typeDescKey']) for play in plays if play['typeCode'] in new_event_codes)

        for tup in new_event_tuples:
            ref_types.import_event_type(tup)

    # Insert events
    for event in plays:
        play_obj = Event()
        play_obj.from_dict(event)
        play_objs.append(play_obj)

    try:
        db.session.add_all(play_objs)
        db.session.commit()
        logger.info('Events Inserted for Game %(gameID)d')
    except IntegrityError as e:
        db.session.rollback()
        logger.error('Failed to insert events for Game %(gameID)d')
        logger.debug(e.statement)
        logger.debug(e.orig)

def delete_all_games():
    Game.query.delete()
    db.session.commit()
    logger.info('Deleted ALL Games')

def delete_all_player_games():
    PlayerGame.query.delete()
    db.session.commit()
    logger.info('Deleted ALL Appearances')

def delete_all_events(gameID = None):
    if gameID is not None:
        Event.query.filter_by(gameID=gameID).delete()
        logger.info('Deleted events for Game %(gameID)d')
    else:
        Event.query.delete()
        logger.info('Deleted ALL Events')
    db.session.commit()


if __name__ == "__main__":
    app.app_context().push()
    # import_games(datetime.today() - timedelta(days=1))
    # import_play_by_play(2024020170)
    insert_rosters(2024020170)
    # delete_all_player_games()
    # delete_all_events(2024020170)