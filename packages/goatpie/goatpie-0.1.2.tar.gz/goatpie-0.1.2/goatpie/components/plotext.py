from rich.ansi import AnsiDecoder
from rich.console import Console, Group
from rich.jupyter import JupyterMixin

from ..helpers import render_stats


class plotextRenderable(JupyterMixin):
    """
    'Rich' renderable for plots created with 'plotext'
    """

    def __init__(self, obj, limit: int) -> None:
        """
        Initializes 'plotextRenderable' instance

        :param obj: goatpie.GoatPie
        :param limit: int Limits data being displayed

        :return: None
        """

        # Set plotter & settings
        self.obj = obj
        self.limit = limit

        # Implement decoder
        self.decoder = AnsiDecoder()


    def __rich_console__(self, console: Console, options: dict) -> None:
        """
        Creates canvas for display in the console

        :param console: Console
        :param options: dict

        :return: None
        """

        self.width = options.max_width or console.width
        self.height = options.height or console.height

        canvas = render_stats(self.obj, self.width, self.height, limit=self.limit)
        self.rich_canvas = Group(*self.decoder.decode(canvas))

        yield self.rich_canvas
