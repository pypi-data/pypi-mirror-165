from typing import Optional

from rich.ansi import AnsiDecoder
from rich.console import Console
from rich.padding import Padding, PaddingDimensions
from rich.panel import Panel
from textual.widget import Widget

from .plotext import plotextRenderable


class GoatBar(Widget):
    """
    Textual widget for 'multiple_bar' plot created with 'plotext'
    """

    def __init__(self, obj, name: Optional[str] = None, limit: int = 14
    ) -> None:
        """
        Initializes 'GoatBar' instance

        :param obj: goatpie.GoatPie
        :param name: str
        :param limit: int Limits data being displayed

        :return: None
        """

        # Initialize parent
        super().__init__(name)

        # Set plotter & settings
        self.obj = obj
        self.limit = limit


    def render(self) -> Panel:
        """
        Renders 'multiple_bar' plot created with 'plotext'

        :return: rich.panel.Panel
        """

        # Create 'rich' element
        renderable = plotextRenderable(self.obj, self.limit)

        # Define top padding
        spacing = (1, 0, 0, 0)

        return Padding(Panel(renderable, title='Last {} days'.format(self.limit), padding=spacing), spacing)


    # TODO: Update data & rerender
    # async def update(self, renderable: RenderableType) -> None:
    #     self.renderable = renderable
    #     self.refresh()
