import click
import requests
import logfire

from src.main import BACKEND_URL
from src.scrapers.events import post_event_types
from src.scrapers.teams import scrape_teams, post_teams

@click.group()
def setup():
    """Statcheck DB Setup CLI"""
    pass

@setup.command('init-db')
@logfire.instrument('INITIALISING DB')
def init_db():
    post_event_types()
    teams = scrape_teams()
    post_teams(teams)
    r = requests.get(f"{BACKEND_URL}/admin/init-views")
    logfire.info(f'View Initialisation: {r.status_code}', response_code=r.status_code)

if __name__ == '__main__':
    setup()