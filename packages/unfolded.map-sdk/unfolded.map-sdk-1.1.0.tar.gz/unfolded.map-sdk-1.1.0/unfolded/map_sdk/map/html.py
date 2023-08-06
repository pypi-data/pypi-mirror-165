from pathlib import Path
from typing import Optional, Union

from unfolded.map_sdk.map.base import BaseNonInteractiveMap
from unfolded.map_sdk.transport.html import HTMLTransport

TEMPLATE_DIR = (Path(__file__).parent / ".." / "templates").resolve()


class HTMLMap(BaseNonInteractiveMap):
    transport: HTMLTransport

    map_url: Optional[str]
    map_uuid: Optional[str]
    width: Optional[Union[str, int, float]]
    height: Optional[Union[str, int, float]]

    def __init__(
        self,
        *,
        map_url: Optional[str] = None,
        map_uuid: Optional[str] = None,
        width: Optional[Union[str, int, float]] = None,
        height: Optional[Union[str, int, float]] = None,
    ):
        super().__init__()
        self.map_url = map_url
        self.map_uuid = map_uuid
        self.width = width
        self.height = height
        self.transport = HTMLTransport()
        self.rendered = False

    def _repr_html_(self) -> str:
        return self.render()

    def render(self) -> str:
        return self.transport.render_template()
