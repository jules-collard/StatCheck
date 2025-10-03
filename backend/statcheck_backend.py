from app import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so

@app.shell_context_processor
def make_shell_context():
    return {'sa':sa, 'so':so, 'db':db }