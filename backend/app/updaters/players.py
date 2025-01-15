from app import app, db
from app.scrapers import scrape_player
from app.models import Player
from sqlalchemy.exc import IntegrityError

def insert_or_update_player(id: int):
    player_data = scrape_player(id)
    player = Player()
    player.from_dict(player_data)

    try:
        db.session.merge(player)
        db.session.commit()
        print(f"{player} inserted/updated")
    except IntegrityError:
        db.session.rollback()
        print(f"Database Integrity Error")

def delete_all_players():
    Player.query.delete()
    db.session.commit()

def delete_player(id: int):
    Player.query.filter_by(id=id).delete()

if __name__ == "__main__":
    app.app_context().push()
    insert_or_update_player(8478402)