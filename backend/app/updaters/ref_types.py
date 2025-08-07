from app import app, db
from app.models import GameType, EventType
from app.updaters import log_error

from sqlalchemy.exc import IntegrityError

def insert_game_types():
    pre = GameType()
    pre.from_dict({"typeCode": 1, "typeDescKey": "PRE"})
    reg = GameType()
    reg.from_dict({"typeCode": 2, "typeDescKey": "REG"})
    post = GameType()
    post.from_dict({"typeCode": 3, "typeDescKey": "POST"})
    fourNations = GameType()
    fourNations.from_dict({"typeCode": 19, "typeDescKey": "4NFO"})
    fourNationsFinal = GameType()
    fourNationsFinal.from_dict({"typeCode": 20, "typeDescKey": "4NFOFINAL"})
    

    try:
        db.session.merge(pre)
        db.session.merge(reg)
        db.session.merge(post)
        db.session.merge(fourNations)
        db.session.merge(fourNationsFinal)
        db.session.commit()
        app.logger.info('Game Types Inserted')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning('Failed to Inserted Game Types')
        log_error(e)

def insert_event_type(tup: tuple[int, str]):
    event = EventType()
    event.from_tuple(tup)

    try:
        db.session.add(event)
        db.session.commit()
        app.logger.info(f'Inserted {event}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert {event}')
        log_error(e)

def delete_all_event_types():
    EventType.query.delete()
    db.session.commit()
    app.logger.info(f'Deleted ALL Event Types')

def delete_all_game_types():
    GameType.query.delete()
    db.session.commit()
    app.logger.info(f'Deleted ALL Game Types')