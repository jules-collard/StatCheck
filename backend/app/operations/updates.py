from datetime import datetime

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
@click.option('-i', '--id', type=int)
@click.option('-x', '--xg', type=bool)
def import_game(id: int, xg: bool):
    g.import_game(id, calc_xg=xg)

@games.command('import-date')
@click.option('-d', '--date', default=datetime.today().strftime('%Y-%m-%d'), type=str)
def import_games_date(date: str):
    g.import_games_on_date(date)

@games.command('import-range')
@click.option('-d', '--date', type=(str,str))
def import_games_range(date_tup: tuple[str]):
    g.import_games_date_range(date_tup[0], date_tup[1])

@games.command('fix')
def fix_games():
    g.import_games_from_errors()

@games.command('remove')
@click.option('-i', '--id', type=int)
def remove_game(id: int):
    g.remove_game(id)

if __name__ == '__main__':
    with app.app_context():
        cli()