from sqlalchemy.exc import IntegrityError
from app import app

def log_error(e: IntegrityError):
    app.logger.error(e.statement)
    app.logger.error(e.orig)