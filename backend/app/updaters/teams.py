from sqlite3 import IntegrityError
from app import scrapers
from app import app, db
from app.models import Team

def import_teams():
    team_dicts = scrapers.scrape_teams()
    team_objects = []

    for attrs in team_dicts:
        team = Team()
        team.from_dict(attrs)
        team_objects.append(team)

    try:
        db.session.add_all(team_objects)
        db.session.commit()
        print("Teams successfully imported")
    except IntegrityError:
        db.session.rollback()
        print("Unsuccessful import")

def delete_all_teams():
    Team.query.delete()
    db.session.commit()

if __name__ == "__main__":
    app.app_context().push()
    import_teams()