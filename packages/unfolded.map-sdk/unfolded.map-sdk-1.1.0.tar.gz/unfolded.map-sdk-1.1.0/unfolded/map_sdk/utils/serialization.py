import logging
from typing import Dict, List, Optional, Tuple

from unfolded.map_sdk.api.base import Action
from unfolded.map_sdk.utils.encoders import jsonable_encoder


def serialize_action(action: Action) -> Tuple[Dict, Optional[List[bytes]]]:
    """Serialize Action to format that can be sent through Jupyter Comm mechanism"""
    # Use FastAPI's encoder to serialize to dict directly, without going through json
    # https://fastapi.tiangolo.com/tutorial/encoder/
    # https://stackoverflow.com/a/68778590
    d = jsonable_encoder(action, by_alias=True, exclude_none=True)

    # We want all keys except for `type` and `messageId` to be within a top-level `data` key

    # Make sure the args key doesn't exist yet
    if d.get("args") != None:
        logging.debug("args key already exists")

    # We define new objects instead of assigning to `d` immediately so that an attribute of the
    # action can be named `args` or `options`
    new_args = []
    new_options = {}

    # Keys that should stay at the top level
    top_level_json_keys = ["type", "messageId"]

    options_keys = list(map(action.Config.alias_generator, action.Meta.options))

    # Get all non-top-level non-options argument keys
    model_keys = set(d.keys()).difference(top_level_json_keys).difference(options_keys)

    # Transform listed args to (usually CamelCase) aliases
    arg_keys = list(map(action.Config.alias_generator, action.Meta.args))

    if model_keys != set(arg_keys):
        mismatched_keys = model_keys.symmetric_difference(arg_keys)
        logging.debug(
            f"Mismatch between args list and model fields in model {action.__class__.__name__}: {mismatched_keys}"
        )

    # Add arguments to args list
    for key in arg_keys:
        new_args.append(d.pop(key))

    # Add options to options dict
    for key in options_keys:
        val = d.pop(key)
        if val is not None:
            new_options[key] = val

    d["args"] = new_args

    # Don't send options if empty
    if new_options:
        d["options"] = new_options

    # Not currently using binary Comm message transfer
    return d, None
