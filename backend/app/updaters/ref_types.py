from app import app, db
from app.models import GameType, EventType
from sqlalchemy.exc import IntegrityError

def import_game_types():
    reg = GameType()
    reg.from_dict({"typeCode": 2, "typeDescKey": "REG"})
    post = GameType()
    post.from_dict({"typeCode": 3, "typeDescKey": "POST"})

    try:
        db.session.add(reg)
        db.session.add(post)
        db.session.commit()
        print("Game types successfully imported")
    except IntegrityError:
        db.session.rollback()
        print("Unsuccessful import")


def import_event_type(typeCode: int, typeDescKey: str):
    event = EventType()
    event.from_dict({"typeCode": typeCode, "typeDescKey": typeDescKey})

    try:
        db.session.add(event)
        db.session.commit()
        print(f"<{typeDescKey}> event successfully imported")
    except IntegrityError:
        db.session.rollback()
        print("Unsuccessful import")

def clear_all_event_types():
    EventType.query.delete()
    db.session.commit()

def delete_all_game_types():
    GameType.query.delete()
    db.session.commit()

if __name__ == "__main__":
    app.app_context().push()
    import_game_types()