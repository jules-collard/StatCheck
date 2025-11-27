from typing import List
from datetime import datetime, timedelta

import click
import requests
import logfire

from src.main import BACKEND_URL
from src.scrapers.games import scrape_schedule, post_game
from src.scrapers.appearances import scrape_appearances, post_appearances
from src.scrapers.events import scrape_pbp, post_pbp
from src.scrapers.shifts import scrape_shifts, post_shifts
from src.analytics.onice.updating import get_split_shifts, post_split_shifts
from src.models.games import GameBase

@click.group()
def daily():
    """StatCheck Daily DB-Updates CLI"""
    pass

def import_game(game: GameBase):
    post_game(game)

    skater_apps, goalie_apps = scrape_appearances(game.id)
    post_appearances(game.id, skater_apps, goalie_apps)

    pbp = scrape_pbp(game.id, neutralSite=game.neutralSite)
    post_pbp(game.id, pbp)

    shifts = scrape_shifts(game.id)
    post_shifts(game.id, shifts)

    split_shifts = get_split_shifts(shifts)
    post_split_shifts(game.id, split_shifts)

@daily.command('import-gameday')
@click.option('-d', '--date', default=(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), type=str)
@logfire.instrument('Importing Games on {date=}')
def import_games_date(date: str):
    games: List[GameBase] = scrape_schedule(date)
    for game in games:
        import_game(game)
    requests.get(f"{BACKEND_URL}/admin/refresh-views")

@daily.command('import-daterange')
@click.argument('start', type=str)
@click.argument('end', type=str)
@logfire.instrument('Importing Games from {start=} to {end=}')
def import_games_date_range(start: str, end: str):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    while start_date <= end_date:
        games: List[GameBase] = scrape_schedule(start_date.strftime('%Y-%m-%d'))
        with logfire.span(f'Date: {start_date.date()}'):
            for game in games:
                import_game(game)
        start_date += timedelta(days=1)
    
    r = requests.get(f"{BACKEND_URL}/admin/refresh-views")
    logfire.info(f'REFRESHED VIEWS: {r.status_code}', response_code=r.status_code)

@daily.command('import-game')
@click.option('-i', '--id', type=int)
@click.option('-d', '--date', type=str)
def import_game_id(id: int, date: str):
    games: List[GameBase] = scrape_schedule(date)
    game_with_id = [g for g in games if g.id == id]
    game = game_with_id[0] if len(game_with_id) > 0 else None
    if game:
        import_game(game)


if __name__ == '__main__':
    daily()