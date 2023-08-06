import getpass
import os

import click

from .app import GoatPieApp
from .goatpie import GoatPie


@click.command()
@click.argument('url')
@click.option('-u', '--update', is_flag=True, help='Initiates update of local database')
@click.option('-l', '--limit', default=14, help='Shows visits & pageviews in the last XY days')
@click.version_option('0.1.0')
def cli(url: str, update: bool, limit: int) -> None:
    """
    Provides 'Goatcounter' statistics for URL
    """

    # Retrieve API token
    token = os.environ.get('GOATPIE_TOKEN', None)

    if token is None:
        token = getpass.getpass('Please enter your token: ')

    # Determine base directory
    base_dir = click.get_app_dir('goatpie')

    # Get ready
    obj = GoatPie(url, token, base_dir)

    # If specified ..
    if update:
        # .. force database update
        obj.update(0)

    # Create application
    app = GoatPieApp

    # Configure it
    app.obj = obj
    app.limit = limit

    # Run!
    app.run(title='"Goatcounter" analytics', log=os.path.join(base_dir, 'app.log'))
