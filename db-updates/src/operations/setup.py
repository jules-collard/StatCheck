import click
import requests

from .. import BACKEND_URL
from src.scrapers.events import post_event_types
from src.scrapers.teams import scrape_teams, post_teams

@click.group()
def setup():
    """Statcheck DB Setup CLI"""
    pass

@setup.command('init-db')
def init_db():
    post_event_types()
    teams = scrape_teams()
    post_teams(teams)
    requests.get(f"{BACKEND_URL}/admin/init-views")

if __name__ == '__main__':
    setup()