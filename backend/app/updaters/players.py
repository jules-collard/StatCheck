from app import app,db
from app.scrapers import scrape_player
from app.models import Player, Award
from app.updaters import log_error

from sqlalchemy.exc import IntegrityError
from requests.exceptions import HTTPError

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

    for awardName, seasons in player_awards.items():
        for season in seasons:
            award = Award(**{'awardName':awardName, 'season': season, 'winningPlayerID':id})
            db.session.merge(award)
            db.session.commit()
            app.logger.info(f'Added {season} {awardName}')

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