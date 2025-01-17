from app import scrapers
from app import db
from app.models import Team
from app.updaters import logger, log_error

from sqlalchemy.exc import IntegrityError

def insert_teams():
    logger.info('Inserting Teams')
    team_dicts = scrapers.scrape_teams()
    team_objects = []

    for attrs in team_dicts:
        team = Team()
        team.from_dict(attrs)
        team_objects.append(team)

    try:
        db.session.add_all(team_objects)
        db.session.commit()
        logger.info('Inserted Teams')
    except IntegrityError as e:
        db.session.rollback()
        logger.error('Failed to Insert Teams')
        log_error(e)

def delete_all_teams():
    Team.query.delete()
    db.session.commit()
    logger.info('Deleted ALL Teams')