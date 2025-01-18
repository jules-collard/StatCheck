from app import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import data_updates as du

@app.shell_context_processor
def make_shell_context():
    return {'sa':sa, 'so':so, 'db':db, 'du':du }