from requests.exceptions import HTTPError
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.scrapers import scrape_pbp
from app.models import GameImportError, Event, EventType
from app.inserters import log_error, ref_types

def insert_events(gameID: int, check_new_event_codes=False):
    try:
        plays = scrape_pbp(gameID)
    except HTTPError as e:
        app.logger.warning(f'Events not found for Game {gameID}')
        app.logger.error(e)
        db.session.add(GameImportError(gameID, "PBP"))
        db.session.commit()
        # app.logger.info(f'Trying pbp with boxscores for Game {gameID}')
        # try:
        #     plays = scrape_pbp_boxscore(gameID)
        # except HTTPError as box_e:
        #     app.logger.warning(f'Boxscore not found for Game {gameID}')
        #     app.logger.error(box_e)
        #     db.session.add(GameImportError(gameID, "BOX"))
        #     db.session.commit()
        #     return

    # Add new event codes if not already in database
    if check_new_event_codes:
        existing_event_codes = set(i[0] for i in db.session.query(EventType.typeCode).all())
        new_event_codes = set(play.get('typeCode') for play in plays) - existing_event_codes
        if len(new_event_codes) > 0:
            app.logger.warning(f'New Event Types: {new_event_codes} (GameID: {gameID})')
    
    for play in plays:
        play.pop('typeDescKey')

    # Insert events
    play_objs = [Event(**play) for play in plays]

    try:
        db.session.add_all(play_objs)
        db.session.commit()
        app.logger.info(f'Events Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert events for Game {gameID}')
        log_error(e)

def delete_events(gameID = None):
    if gameID is not None:
        Event.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted events for Game {gameID}')
    else:
        Event.query.delete()
        app.logger.info('Deleted ALL Events')
    db.session.commit()