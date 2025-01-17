from app import db
from app.models import GameType, EventType
from app.updaters import logger, log_error

from sqlalchemy.exc import IntegrityError

def insert_game_types():
    reg = GameType()
    reg.from_dict({"typeCode": 2, "typeDescKey": "REG"})
    post = GameType()
    post.from_dict({"typeCode": 3, "typeDescKey": "POST"})

    try:
        db.session.add(reg)
        db.session.add(post)
        db.session.commit()
        logger.info('Game Types Inserted')
    except IntegrityError as e:
        db.session.rollback()
        logger.error('Failed to Inserted Game Types')
        log_error(e)

def insert_event_type(tup: tuple[int, str]):
    event = EventType()
    event.from_tuple(tup)

    try:
        db.session.add(event)
        db.session.commit()
        logger.info(f'Inserted {event}')
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f'Failed to insert {event}')
        log_error(e)

def delete_all_event_types():
    EventType.query.delete()
    db.session.commit()
    logger.info(f'Deleted ALL Event Types')

def delete_all_game_types():
    GameType.query.delete()
    db.session.commit()
    logger.info(f'Deleted ALL Game Types')