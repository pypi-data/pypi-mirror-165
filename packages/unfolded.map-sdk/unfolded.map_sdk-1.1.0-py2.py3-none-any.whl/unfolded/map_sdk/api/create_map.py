from typing import Any, Optional

from unfolded.map_sdk.environment import CURRENT_ENVIRONMENT, Environment
from unfolded.map_sdk.map import SyncWidgetMap

__all__ = ("create_map",)


def create_map(*, html: Optional[bool] = None, **kwargs: Any) -> SyncWidgetMap:
    """Create an unfolded map

    Args:
        html (Optional[bool], optional): Whether to create a pure HTML map. Defaults to None.
    """
    if html or CURRENT_ENVIRONMENT == Environment.DATABRICKS:
        raise NotImplementedError("Static HTML map not yet implemented")
        # return HTMLMap(**kwargs)

    return SyncWidgetMap(**kwargs)
