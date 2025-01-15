from app import app, db
from app.models import GameType, EventType
from sqlalchemy.exc import IntegrityError

def import_game_types():
    reg = GameType().from_dict({"typeCode": 2, "typeDescKey": "REG"})
    post = GameType().from_dict({"typeCode": 3, "typeDescKey": "POST"})

    try:
        db.session.add(reg)
        db.session.add(post)
        db.session.commit()
        print("Game types successfully imported")
    except IntegrityError:
        db.session.rollback()
        print("Unsuccessful import")


def import_event_type(typeCode: int, typeDescKey: str):
    event = EventType().from_dict({"typeCode": typeCode, "typeDescKey": typeDescKey})

    try:
        db.session.add(event)
        db.session.commit()
        print(f"<{typeDescKey}> event successfully imported")
    except IntegrityError:
        db.session.rollback()
        print("Unsuccessful import")
