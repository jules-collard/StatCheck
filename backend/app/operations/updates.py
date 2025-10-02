from datetime import datetime, timedelta

import click

from app import app
from . import games as g

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
@click.option('-i', '--id', prompt=True, type=int)
def remove_game(id: int):
    if id is None:
        click.Abort()
    g.remove_game(id)

if __name__ == '__main__':
    app.app_context().push()
    cli()