from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app import app, db
from app.scrapers import scrape_schedule
from app.models import Game
from app.updaters import log_error

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

def delete_games(*ids: int):
    if len(ids) == 0:
        Game.query.delete()
        app.logger.info('Deleted ALL Games')
    else:
        Game.query.filter(Game.id.in_(ids)).delete()
        app.logger.info(f'Deleted games {ids}')
    db.session.commit()
