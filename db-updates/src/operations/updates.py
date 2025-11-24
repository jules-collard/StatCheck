import click

from src.scrapers.events import patch_xg

@click.group()
def updates():
    """Statcheck DB Updates CLI"""
    pass

@updates.command('patch-xg')
@click.option('-i', '--id', type=int)
def update_xg(id: int):
    patch_xg(id)

if __name__ == '__main__':
    updates()