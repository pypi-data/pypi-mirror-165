from typing import Dict, List, Optional

from ipywidgets import DOMWidget
from pydantic import AnyHttpUrl
from traitlets import Dict as TraitletsDict
from traitlets import Unicode

from unfolded.map_sdk._frontend import module_name, module_version
from unfolded.map_sdk._version import __version__
from unfolded.map_sdk.api.base import CamelCaseBaseModel
from unfolded.map_sdk.api.map_api import MapStyleCreationProps
from unfolded.map_sdk.environment import default_height
from unfolded.map_sdk.map.base import BaseInteractiveMap
from unfolded.map_sdk.transport.widget import BlockingWidgetTransport


class BasemapParams(CamelCaseBaseModel):
    custom_map_styles: Optional[List[MapStyleCreationProps]]
    initial_map_style_id: Optional[str]


class RasterParams(CamelCaseBaseModel):
    server_urls: Optional[List[AnyHttpUrl]]


DEFAULT_MAP_STYLE = {
    "height": default_height(),
    "width": "100%",
}


class SyncWidgetMap(DOMWidget, BaseInteractiveMap):
    _model_name = Unicode("UnfoldedMapModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("UnfoldedMapView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    style = TraitletsDict().tag(sync=True)
    basemaps = TraitletsDict().tag(sync=True)
    raster = TraitletsDict().tag(sync=True)
    _internal = TraitletsDict().tag(sync=True)

    # Note: We define an unused kwargs so that an error is not produced for invalid initialization
    # args between the widget and HTML implementations
    def __init__(
        self,
        *,
        style: Optional[Dict] = None,
        basemaps: Optional[Dict] = None,
        raster: Optional[Dict] = None,
        _internal: Optional[Dict] = None,
        **kwargs  # pylint: disable=unused-argument
    ):
        """Initializes a new widget map

        Kwargs:
            style: Optional map container CSS style customization. Uses camelCase as this is React standard.
            basemaps: Basemap customization settings.
            raster: Customization related to raster datasets and tiles.

        """
        super().__init__()
        self.transport = BlockingWidgetTransport(widget=self)

        if style:
            self.style = {**DEFAULT_MAP_STYLE, **style}
        else:
            self.style = DEFAULT_MAP_STYLE

        if basemaps:
            validated_basemaps = BasemapParams(**basemaps)
            self.basemaps = validated_basemaps.dict(by_alias=True, exclude_none=True)

        if raster:
            validated_raster = RasterParams(**raster)
            self.raster = validated_raster.dict(by_alias=True, exclude_none=True)

        if _internal:
            self._internal = _internal

        on_msg = lambda widget, content, buffers: self.transport.receive_message(
            content, buffers
        )
        self.on_msg(on_msg)
        self._is_loaded = False

    def render(self) -> None:
        raise NotImplementedError()
