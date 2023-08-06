import abc
from typing import Optional, Union

from unfolded.map_sdk.api.dataset_api import (
    DatasetApiInteractiveMixin,
    DatasetApiNonInteractiveMixin,
)
from unfolded.map_sdk.api.event_api import EventApiInteractiveMixin
from unfolded.map_sdk.api.filter_api import (
    FilterApiInteractiveMixin,
    FilterApiNonInteractiveMixin,
)
from unfolded.map_sdk.api.layer_api import (
    LayerApiInteractiveMixin,
    LayerApiNonInteractiveMixin,
)
from unfolded.map_sdk.api.map_api import (
    MapApiInteractiveMixin,
    MapApiNonInteractiveMixin,
)
from unfolded.map_sdk.transport.base import (
    BaseInteractiveTransport,
    BaseNonInteractiveTransport,
    BaseTransport,
)


class BaseMap:
    """
    Base class for all map types (both widget and non-widget)
    """

    transport: BaseTransport

    @abc.abstractmethod
    def __init__(
        self,
        *,
        map_url: Optional[str] = None,
        map_uuid: Optional[str] = None,
        width: Optional[Union[str, int, float]] = None,
        height: Optional[Union[str, int, float]] = None,
    ):
        pass


class BaseInteractiveMap(
    BaseMap,
    MapApiInteractiveMixin,
    DatasetApiInteractiveMixin,
    FilterApiInteractiveMixin,
    LayerApiInteractiveMixin,
    EventApiInteractiveMixin,
):
    transport: BaseInteractiveTransport
    pass


class BaseNonInteractiveMap(
    BaseMap,
    MapApiNonInteractiveMixin,
    DatasetApiNonInteractiveMixin,
    FilterApiNonInteractiveMixin,
    LayerApiNonInteractiveMixin,
):
    transport: BaseNonInteractiveTransport
    pass
