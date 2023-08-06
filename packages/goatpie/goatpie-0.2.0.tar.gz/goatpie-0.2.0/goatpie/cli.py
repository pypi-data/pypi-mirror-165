import configparser
import os

import click

from .app import GoatPieApp
from .goatpie import GoatPie
from .helpers import get_domain


@click.command()
@click.argument("url")
@click.option("-u", "--update", is_flag=True, help="Initiates update of local database")
@click.option("-l", "--limit", default=14, help="Shows visits & pageviews in the last XY days")
@click.version_option("0.2.0")
def cli(url: str, update: bool, limit: int) -> None:
    """
    Provides 'Goatcounter' statistics for URL
    """

    # Determine base directory
    base_dir = click.get_app_dir("goatpie")

    # Define minimum update interval (in seconds)
    interval = 1 * 60 * 60  # 1 hour

    # Initialize config object (using defaults)
    config = configparser.SafeConfigParser(defaults={"interval": interval})

    # Get path to config file
    config_file = os.path.join(base_dir, "config.ini")

    # If not existent ..
    if not os.path.exists(config_file):
        # .. create it (using default values)
        with open(config_file, "w") as file:
            config.write(file)

    # Load its contents
    config.read(config_file)

    # Get domain identifier
    domain = get_domain(url, True)

    # If no section for domain ..
    if domain not in config:
        # .. create it & add interval option
        config.add_section(domain)
        config.set(domain, "interval", str(interval))

    # If no API token for domain section ..
    if not config.has_option(domain, "token"):
        # .. retrieve it
        token = click.prompt("Please enter your token", hide_input=True, confirmation_prompt=True)

        # If approved ..
        if click.confirm("Save token for later?", default=True):
            # (1) .. save API token
            config.set(domain, "token", token)

            # (2) .. update config file
            with open(config_file, "w") as file:
                config.write(file)

    # Get ready
    obj = GoatPie(url, config[domain].get("token"), base_dir)
    obj.interval = int(config[domain].get("interval", interval))

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
    app.run(title='"Goatcounter" analytics', log=os.path.join(base_dir, "app.log"))
