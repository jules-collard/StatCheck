from app import app, db
from app.scrapers import scrape_schedule, scrape_rosters, scrape_pbp
from app.models import Game, PlayerGame, Event, EventType
from app.updaters.ref_types import import_event_type

from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

def import_games(date: datetime):
    game_dicts = scrape_schedule(date.date().strftime("%Y-%m-%d"))
    game_objects = []

    for game_dets in game_dicts:
        game = Game()
        game.from_dict(game_dets)
        game_objects.append(game)

    try:
        db.session.add_all(game_objects)
        db.session.commit()
        print(f"{date.date().strftime("%Y-%m-%d")} Games Imported")
    except IntegrityError:
        db.session.rollback()
        print("Unsuccessful import")

def import_rosters(gameID: int, insert_new_player=True):
    player_games = scrape_rosters(gameID)
    player_game_objs = []

    for appearance in player_games:
        player_game = PlayerGame()
        player_game.from_dict(appearance)
        player_game_objs.append(player_game)

    try:
        db.session.add_all(player_game_objs)
        db.session.commit()
        print(f"Rosters for Game {gameID} Imported")
    except IntegrityError:
        db.session.rollback()
        print(f"Unsuccessful roster import for game {gameID}")

def import_play_by_play(gameID: int, insert_new_event_codes=True):
    plays = scrape_pbp(gameID)
    play_objs = []

    if insert_new_event_codes:
        # Add new event codes if not already in database
        existing_event_codes = set(i[0] for i in db.session.query(EventType.typeCode).all())
        print(existing_event_codes)
        new_event_codes = set(play['typeCode'] for play in plays) - existing_event_codes
        print(new_event_codes)
        new_event_tuples = set((play['typeCode'],play['typeDescKey']) for play in plays if play['typeCode'] in new_event_codes)

        for tup in new_event_tuples:
            import_event_type(tup)

    # Insert events
    for event in plays:
        play_obj = Event()
        play_obj.from_dict(event)
        play_objs.append(play_obj)

    try:
        db.session.add_all(play_objs)
        db.session.commit()
        print(f"Events for Game {gameID} Imported")
    except IntegrityError:
        db.session.rollback()
        print(f"Unsuccessful event import for game {gameID}")

def delete_all_games():
    Game.query.delete()
    db.session.commit()

def delete_all_player_games():
    PlayerGame.query.delete()
    db.session.commit()

def delete_all_events(gameID = None):
    if gameID is not None:
        Event.query.filter_by(gameID=gameID).delete()
    else:
        Event.query.delete()
    db.session.commit()


if __name__ == "__main__":
    app.app_context().push()
    # import_games(datetime.today() - timedelta(days=1))
    import_play_by_play(2024020170)
    # delete_all_events(2024020170)