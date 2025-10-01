from requests.exceptions import HTTPError
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.scrapers import scrape_shifts
from app.models import GameImportError, Shift
from app.inserters import log_error

def insert_shifts(gameID: int):
    try:
        shifts = scrape_shifts(gameID)
    except HTTPError as e:
        app.logger.warning(f'Shifts not found for Game {gameID}')
        app.logger.error(e)
        db.session.add(GameImportError(gameID, "SHIFTS"))
        db.session.commit()
        return

    if len(shifts) == 0:
        app.logger.warning(f'No shift data for Game {gameID}')
        db.session.add(GameImportError(gameID, "SHIFTS"))
        db.session.commit()
        return

    shift_objs = [Shift(**shift) for shift in shifts]

    try:
        db.session.add_all(shift_objs)
        db.session.commit()
        app.logger.info(f'Shifts Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert shifts for Game {gameID}')
        log_error(e)

def delete_shifts(gameID = None):
    if gameID is not None:
        Shift.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted shifts for Game {gameID}')
    else:
        Shift.query.delete()
        app.logger.info('Deleted ALL Shifts')
    db.session.commit()