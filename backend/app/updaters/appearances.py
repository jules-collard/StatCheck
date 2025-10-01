from requests.exceptions import HTTPError
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.scrapers import scrape_appearances_boxscore
from app.models import Player, GameImportError, SkaterAppearance, GoalieAppearance
from app.updaters import log_error, players

def insert_appearances(gameID: int):
    try:
        skater_appearances, goalie_appearances = scrape_appearances_boxscore(gameID)
    except HTTPError as e:
        app.logger.warning(f'Boxscores not found for Game {gameID}')
        app.logger.error(e)
        db.session.add(GameImportError(gameID, "BOX"))
        db.session.commit()
        return
    
    skater_appearances_obj = [SkaterAppearance(**appearance) for appearance in skater_appearances]
    goalie_appearances_obj = [GoalieAppearance(**appearance) for appearance in goalie_appearances]

    try:
        for appearance in skater_appearances_obj + goalie_appearances_obj:
            db.session.merge(appearance)
        db.session.commit()
        app.logger.info(f'Appearances Inserted for Game {gameID}')
    except IntegrityError as e:
        db.session.rollback()
        app.logger.warning(f'Failed to insert Appearances for Game {gameID}')
        log_error(e)

    # Add new players to database
    existing_player_ids = set(player.id for player in Player.query.all())
    new_player_ids = set(appearance.playerID for appearance in skater_appearances_obj + goalie_appearances_obj) - existing_player_ids
    for id in new_player_ids:
        players.insert_or_update_player(id)

def delete_appearances(gameID: int = None):
    delete_goalie_appearances(gameID)
    delete_skater_appearances(gameID)

def delete_goalie_appearances(gameID = None):
    if gameID is not None:
        GoalieAppearance.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted goalie appearances for Game {gameID}')
    else:
        GoalieAppearance.query.delete()
        app.logger.info('Deleted ALL Goalie Appearances')
    db.session.commit()

def delete_skater_appearances(gameID = None):
    if gameID is not None:
        SkaterAppearance.query.filter_by(gameID=gameID).delete()
        app.logger.info(f'Deleted skater appearances for Game {gameID}')
    else:
        GoalieAppearance.query.delete()
        app.logger.info('Deleted ALL Skater Appearances')
    db.session.commit()