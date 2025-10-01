from sqlalchemy.exc import IntegrityError

from app import scrapers
from app import app, db
from app.models import Team
from app.updaters import log_error

def insert_teams():
    team_dicts = scrapers.scrape_teams()
    team_objects = [Team(**team_dict) for team_dict in team_dicts]

    try:
        for team in team_objects:
            db.session.merge(team)
        db.session.commit()
        app.logger.info('Inserted/Updated Teams')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning('Failed to Insert/Update Teams')
        log_error(e)

def delete_all_teams():
    Team.query.delete()
    db.session.commit()
    app.logger.info('Deleted ALL Teams')