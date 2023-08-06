import click

from . import __version__
from .client.http.api import Api


@click.command()
@click.version_option(version=__version__)
def main():
    """The hypermodern Python project."""
    click.echo("Blockbax SDK")


@click.command()
@click.version_option(version=__version__)
def user_agent():
    """The hypermodern Python project."""
    click.echo(f"{Api.user_agent}")
