from app import db
from app.scrapers import scrape_player
from app.models import Player
from app.updaters import logger, log_error

from sqlalchemy.exc import IntegrityError
from requests.exceptions import HTTPError

def insert_or_update_player(id: int):
    try:
        player_data = scrape_player(id)
    except HTTPError as e:
        db.session.rollback()
        logger.error(f"Player not found - {id}")
        log_error(e)
        return

    player = Player()
    player.from_dict(player_data)

    try:
        db.session.merge(player)
        db.session.commit()
        logger.info(f'Inserted/Updated {player}')
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f'Failed to Insert/Update {player}')
        log_error(e)

def delete_all_players():
    Player.query.delete()
    db.session.commit()
    logger.info('Deleted ALL Players')

def delete_player(id: int):
    query = Player.query.filter_by(id=id)
    player = query.first()
    query.delete()
    db.session.commit()
    logger.info(f'Deleted {player}')