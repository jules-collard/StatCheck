from datetime import datetime, timedelta

import click

from app import app
from . import games as g
from . import records as r
from . import leaderboards as l

SEASONS = [20102011, 20112012, 20122013, 20132014, 20142015, 20152016, 20162017, 20172018, 20182019, 20192020, 20202021, 20212022, 20222023, 20232024, 20242025, 20252026]

@click.group()
def cli():
    """StatCheck operations CLI"""
    pass

@cli.group()
def games():
    """Game updates"""
    pass

@games.command('import')
@click.option('-i', '--id', prompt=True, type=int)
@click.option('-x', '--xg', default=True, type=bool, help="Calculate XG for Game Events")
def import_game(id: int, xg: bool):
    if id is None:
        click.Abort()
    g.import_game(id, calc_xg=xg)

@games.command('import-date')
@click.option('-d', '--date', default=(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), type=str)
def import_games_date(date: str):
    g.import_games_on_date(date)

@games.command('import-range')
@click.argument('start_date', type=str)
@click.argument('end_date', type=str)
def import_games_range(start_date, end_date):
    g.import_games_date_range(start_date, end_date)

@games.command('fix')
def fix_games():
    g.import_games_from_errors()

@games.command('remove')
@click.option('-i', '--id', prompt=True, type=int, multiple = True)
def remove_game(id: int):
    for gameID in id:
        if id is None:
            click.Abort()
        g.remove_game(gameID)

@cli.group()
def records():
    """Records updates"""
    pass

@records.command('update')
def update_records():
    r.update_all_records()

@cli.group()
def leaderboards():
    """Leaderboard Updates"""
    pass

@leaderboards.command('update-all')
def update_all_leaderboards():
    app.app_context().push()
    for season in SEASONS:
        l.update_skater_leaderboard(season, 2)
        l.update_skater_leaderboard(season, 3)

@leaderboards.command('update-current')
def update_current_leaderboard():
    app.app_context().push()
    season = max(SEASONS)
    l.update_skater_leaderboard(season, 2)
    l.update_skater_leaderboard(season, 3)

if __name__ == '__main__':
    app.app_context().push()
    cli()