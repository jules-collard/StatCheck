import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from requests.exceptions import HTTPError

from app import app,db
from app.scrapers import scrape_player
from app.models import Player, Award
from app.inserters import log_error

def insert_or_update_player(id: int):
    try:
        player_data, player_awards = scrape_player(id)
    except HTTPError as e:
        db.session.rollback()
        app.logger.warning(f"Player not found - {id}")
        app.logger.error(e)
        return

    player = Player(**player_data)

    try:
        db.session.merge(player)
        db.session.commit()
        app.logger.info(f'Inserted/Updated {player}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to Insert/Update {player}')
        log_error(e)
        return

    if len(player_awards) > 0:
        awards = set()
        awards_in_db = set(db.session.scalars(sa.select(Award).where(Award.winningPlayerID == id)).all())
        
        for awardName, seasons in player_awards.items():
            for season in seasons:
                award = Award(**{'awardName':awardName, 'season': season, 'winningPlayerID':id})
                awards.add(award)
        
        awards_to_add = awards - awards_in_db
        
        if len(awards_to_add) > 0:
            db.session.add_all(awards_to_add)
            db.session.commit()
            app.logger.info(f'Added new awards for Player {id}')


def delete_all_players():
    Player.query.delete()
    db.session.commit()
    app.logger.info('Deleted ALL Players')

def delete_player(id: int):
    query = Player.query.filter_by(id=id)
    player = query.first()
    query.delete()
    db.session.commit()
    app.logger.info(f'Deleted {player}')

def update_players():
    ids = [player.id for player in Player.query.all()]
    for id in ids:
        insert_or_update_player(id)