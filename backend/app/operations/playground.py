import sqlalchemy as sa

from app import app, db
from app.models import Player, Game, Event, Shift, GoalieAppearance, SkaterAppearance

if __name__ == "__main__":
    app.app_context().push()
    pass