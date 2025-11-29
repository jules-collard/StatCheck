import click

from src.scrapers.events import scrape_pbp, post_pbp, patch_xg
from src.scrapers.appearances import scrape_appearances, post_appearances
from src.scrapers.shifts import scrape_shifts, post_shifts
from src.analytics.onice.updating import get_split_shifts, post_split_shifts

@click.group()
def updates():
    """Statcheck DB Updates CLI"""
    pass

@updates.command('fix-game')
@click.option('-i', '--id', multiple=True, type=int)
def fix_games(id: tuple[int]):
    for i in id:
        skater_apps, goalie_apps = scrape_appearances(i)
        post_appearances(i, skater_apps, goalie_apps)

        pbp = scrape_pbp(i, neutralSite=False)
        post_pbp(i, pbp)

        shifts = scrape_shifts(i)
        post_shifts(i, shifts)

        split_shifts = get_split_shifts(shifts)
        post_split_shifts(i, split_shifts)


@updates.command('patch-xg')
@click.option('-i', '--id', type=int)
def update_xg(id: int):
    patch_xg(id)

if __name__ == '__main__':
    updates()