from typing import List
from datetime import datetime, timedelta

import click

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
def import_games_date(date: str):
    games: List[GameBase] = scrape_schedule(date)
    for game in games:
        import_game(game)


if __name__ == '__main__':
    daily()