import math
import urllib

import pandas
import plotext

from rich import box
from rich.table import Table, Column


def get_domain(url: str) -> str:
    """
    Extract domain ('example.com'), quick&dirty

    :param url: str Target URL

    :return: str
    """

    # Parse URL & extract its network location
    netloc = urllib.parse.urlparse(url).netloc

    # Combine last two parts (= domain name & tld)
    return '.'.join(netloc.split('.')[-2:])


def render_stats(obj, width: int, height: int,
    labels: list = ['Visits', 'Pageviews'],
    colors: list = ['blue', 'magenta'],
    limit: int = 14,
    step: int = 100
) -> str:
    """
    Renders visits & pageviews using 'plotext'

    :param obj: goatpie.GoatPie
    :param width: int Plot width
    :param height: int Plot height
    :param labels: list Data labels
    :param colors: list Bar colors
    :param limit: int Limits data to last XY days
    :param step: int Steps used on Y-axis

    :return: str Plotted canvas
    """

    # Clear everything
    plotext.clf()
    plotext.clc()

    # Retrieve data
    visits = obj.get_visits(limit)
    pageviews = obj.get_pageviews(limit)

    # Determine relative bar width
    # TODO: Actually calculate something
    bar_width = 0.4

    # Configure plot
    plotext.multiple_bar(visits.Day, [visits.Visits, pageviews.Pageviews], label=labels, width=bar_width, marker='hd', color=colors)
    plotext.plotsize(width, height)
    plotext.xlabel('hits / day')
    plotext.frame(False)
    plotext.ticks_color('white')
    plotext.ticks_style('bold')
    plotext.xticks([])
    plotext.yticks(range(0, pageviews.Pageviews.max(), step))

    return plotext.build()


def data2table(data: pandas.DataFrame, title: str = '', colors = ['blue', 'white', 'cyan']) -> Table:
    """
    Creates 'rich' table from 'pandas' dataframe

    :param data: pandas.DataFrame Table data
    :param title: str Table heading
    :param colors: list Column text colors

    :return: rich.table.Table
    """

    # Create header row
    header = [Column(
        header=header, justify='right', style=colors[idx]
    ) for idx, header in enumerate(data.columns)]

    # Construct table
    table = Table(
        title=title,
        title_style='bold white',
        header_style='bold white',
        show_lines=False,
        box=box.ROUNDED,
        expand=True,
        *header
    )

    # Add rows to it
    for row in data.values:
        table.add_row(*[str(cell) for cell in row])

    return table
