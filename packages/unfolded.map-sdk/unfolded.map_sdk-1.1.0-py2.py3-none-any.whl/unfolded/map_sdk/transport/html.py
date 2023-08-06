from typing import List, Optional, Type

from unfolded.map_sdk.api.base import Action
from unfolded.map_sdk.transport.base import BaseNonInteractiveTransport
from unfolded.map_sdk.types import ResponseClass


class HTMLTransport(BaseNonInteractiveTransport):
    """Transport used in a static HTML map"""

    action_list: List[Action]

    def __init__(self) -> None:
        super().__init__()
        self.action_list = []

    def send_action(
        self,
        *,
        action: Action,
        response_class: Optional[Type[ResponseClass]] = None,
    ) -> None:
        # pylint:disable=unused-argument
        self.action_list.append(action)

    def render_template(self) -> str:
        self.rendered = True
        raise NotImplementedError("Static HTML maps cannot be rendered yet.")
